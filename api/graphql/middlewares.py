class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **args):
        is_authenticated = info.context.user.is_authenticated
        is_mutation = info.operation.operation == "mutation"
        if is_mutation and not is_authenticated:
            return None
        return next(root, info, **args)
