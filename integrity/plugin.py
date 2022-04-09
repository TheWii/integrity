from beet import Context

import integrity as integ


def beet_default(ctx: Context):
    api = ctx.inject(integ.Integrity)
    integ.Component = api.component
