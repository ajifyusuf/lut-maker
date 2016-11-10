import os
import glob
import json
from click.testing import CliRunner

from lut_maker import cli, generate, compute
from lut_maker.constants import *

class TestIntegration:
    def test_single_generation(self, tmpdir):
        name = 'test'
        runner = CliRunner()
        result = runner.invoke(cli.main, ['new', '--name', name, '--data-dir', str(tmpdir)])

        assert result.exit_code == 0
        assert os.path.isfile(str(tmpdir.join(META_FILENAME.format(name))))
        assert os.path.isfile(str(tmpdir.join(ALIGNMENT_FILENAME.format(name))))
        assert os.path.isfile(str(tmpdir.join(MEASUREMENT_FILENAME.format(name,0))))


    def test_stack_generation(self, tmpdir):
        name = 'test'
        stack_size = 5
        runner = CliRunner()
        result = runner.invoke(cli.main, ['new', '--stack', stack_size, '--name', name, '--data-dir', str(tmpdir)])

        for i in range(stack_size):
            assert os.path.isfile(str(tmpdir.join(MEASUREMENT_FILENAME.format(name,i))))

        with open(str(tmpdir.join(META_FILENAME.format(name))),'r') as f:
            data = json.loads(f.read())
            assert len(data['sidecars']) == stack_size


    def test_color_unshuffling(self, tmpdir):
        path = str(tmpdir)
        name = 'test'
        generate.new(17, 1024, path, name, 3)
        lut, meta = compute.compute_lut(path, name)

        with open(str(tmpdir.join(LUT_JSON_FILENAME.format(name))),'r') as f:
            data = json.loads(f.read())

        assert [self.int_sample(sample) for sample in data['samples']] == lut.generate_colors()


    def int_sample(self, sample):
        return [int(channel*255) for channel in sample]
