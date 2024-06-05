import argparse

def dim(min=1, max=None, mod=None):
    """Generate a parser for dimensions."""
    return uint(min=min, max=max, mod=mod)

def prob(min=0.0, max=1.0):
    """Generate a parser for probabilities."""
    def parser(arg):
        try:
            val = float(arg)
        except ValueError:
            raise argparse.ArgumentTypeError('must be a float')
        if min is not None and val < min:
            raise argparse.ArgumentTypeError('must be %d or greater' % min)
        if max is not None and val > max:
            raise argparse.ArgumentTypeError('must be %d or less' % max)
        return val

    return parser

def uint(min=0, max=None, mod=None):
    """Generate a parser for non-negative integers."""
    def parser(arg):
        try:
            val = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError('must be an integer')
        if min is not None and val < min:
            raise argparse.ArgumentTypeError('must be %d or greater' % min)
        if max is not None and val > max:
            raise argparse.ArgumentTypeError('must be %d or less' % max)
        if mod is not None and val % mod != 0:
            raise argparse.ArgumentTypeError('must be divisible by %d' % mod)
        return val

    return parser

def width(max=None):
    """Generate a dimension parser specifically for widths."""
    return dim(min=4, max=max, mod=4)
