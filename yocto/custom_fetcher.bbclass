python () {
    import bb.fetch2
    from bb.fetch2 import FetchMethod
    from bb.fetch2 import logger

    class CustomFetch(FetchMethod):

        def supports(self, ud, d):
            return ud.type in ['custom']

        def recommends_checksum(self, urldata):
            return True

        def urldata_init(self, ud, d):
            raise bb.fetch2.ParameterError("Successfully failed!", ud.url)

        def download(self, ud, d):
            return True

        def checkstatus(self, ud, d):
            return True

    bb.fetch2.methods.append(CustomFetch())
}
