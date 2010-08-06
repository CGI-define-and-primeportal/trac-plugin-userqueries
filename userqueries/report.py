from trac.ticket.report import ReportModule

class LogicaReportModule(ReportModule):
    def process_request(self, req):
        # We don't want to show the user the list that ReportModule implements.
        # We have a better navigation system.
        if not req.args.has_key('id'):
            # TODO: load out of the user preferences
            req.args['id'] = 1
        return ReportModule.process_request(self, req)

