from trac.ticket.report import ReportModule
from trac.web.chrome import add_stylesheet, add_ctxtnav, Chrome
from trac.util.translation import _

class LogicaReportModule(ReportModule):
    def process_request(self, req):
        # We don't want to show the user the list that ReportModule implements.
        # We have a better navigation system.

        req.perm.require('REPORT_VIEW')

        # did the user ask for any special report?
        id = int(req.args.get('id', 1)) # TODO: we should get the default one out of their preferences?
        action = req.args.get('action', 'view')

        data = {}
        if req.method == 'POST':
            if action == 'new':
                self._do_create(req)
            elif action == 'delete':
                self._do_delete(req, id)
            elif action == 'edit':
                self._do_save(req, id)
        elif action in ('copy', 'edit', 'new'):
            template = 'report_edit.html'
            data = self._render_editor(req, id, action=='copy')
            Chrome(self.env).add_wiki_toolbars(req)
        elif action == 'delete':
            template = 'report_delete.html'
            data = self._render_confirm_delete(req, id)
        elif id == -1:
            template, data, content_type = self._render_list(req)
            if content_type: # i.e. alternate format
                return template, data, content_type
        else:
            template, data, content_type = self._render_view(req, id)
            if content_type: # i.e. alternate format
                return template, data, content_type

        # Kludge: only show link to custom query if the query module is actually
        # enabled
        from trac.ticket.query import QueryModule
        if 'TICKET_VIEW' in req.perm and \
                self.env.is_component_enabled(QueryModule):
            add_ctxtnav(req, _('Custom Query'), href=req.href.query())
            data['query_href'] = req.href.query()
        else:
            data['query_href'] = None

        add_stylesheet(req, 'common/css/report.css')
        return template, data, None
