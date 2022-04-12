from beet import Context

import integrity as integ


def beet_default(ctx: Context):
    integ.Component = ctx.inject(integ._Components)
    yield
    integ.Component.generate_tags()
