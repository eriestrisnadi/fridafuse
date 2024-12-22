import pytest
from src.fridafuse import cli
from src.fridafuse.__about__ import __description__, __name__, __version__


def test_create_parser():
    progs = [None, 'xyz', None]
    descriptions = [None, None, 'lorem ipsum dolor']
    parser_args = zip(progs, descriptions)

    for args in parser_args:
        parser = cli.create_parser(*args)
        prog = args[0] if args[0] is not None else __name__
        description = args[1] if args[1] is not None else __description__

        assert parser.prog == prog
        assert parser.description == description
        assert isinstance(parser, cli.argparse.ArgumentParser)

def test_parse_args(capsys):
    known_args = ['-h', '--help']
    unknown_args = ['', '--lipsum', '--arg1', '--arg2']
    err_message = 'error: unrecognized arguments: {}'

    for i, args in enumerate([known_args, unknown_args]):
        for arg in args:
            with pytest.raises(SystemExit):
                cli.parse_args([arg])

            captured = capsys.readouterr()
            result = err_message.format(arg) not in captured.err if i == 0 else err_message.format(arg) in captured.err

            assert result

def test_print_logo(capsys):
    cli.print_logo()
    captured = capsys.readouterr()

    assert cli.logo in captured.out
    assert __version__ in captured.out