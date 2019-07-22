from hashlib import md5


class Store(object):
    async def push(self, other):
        raise NotImplementedError()

    async def pull(self, other):
        raise NotImplementedError()

    async def get_diff(self, other):
        raise NotImplementedError()

    async def get_count(self):
        raise NotImplementedError()

    async def get_data_hash(self):
        raise NotImplementedError()

    async def get_schema_hash(self):
        raise NotImplementedError()

    async def get_signature(self):
        data_hash = self.get_data_hash()
        schema_hash = self.get_schema_hash()
        count = self.get_count()

        data_hash = await data_hash
        schema_hash = await schema_hash
        count = await count
        return f"{data_hash}-{schema_hash}-{count}"


class WithChildren(object):
    async def get_children(self):
        raise NotImplementedError()

    async def get_count(self):
        s = []
        for c in await self.get_children():
            # get counts in parallel
            s.append(c.get_count())

        return sum([await c for c in s])

    async def get_data_hash(self):
        s = []
        for c in await self.get_children():
            # get hashes in parallel
            data_hash = c.get_data_hash()
            s.append((data_hash, c.name))

        return md5(",".join([
            "-".format(await ss[0], ss[1])
            for ss in s
        ]))

    async def get_schema_hash(self):
        s = []
        for c in await self.get_children():
            # get hashes in parallel
            schema_hash = c.get_schema_hash()
            s.append((schema_hash, c.name))

        return md5(",".join([
            "-".format(await ss[0], ss[1])
            for ss in s
        ]))


class ParentStore(WithChildren, Store):
    pass
