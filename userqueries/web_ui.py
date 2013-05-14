# -*- coding: utf-8 -*-
# Copyright (C) 2010 Logica

from trac.core import *
from trac.perm import IPermissionRequestor        
from trac.ticket import TicketSystem, Ticket
from trac.ticket.query import QueryModule
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import ITemplateProvider, Chrome, add_stylesheet
from trac.web.main import IRequestFilter
from genshi.filters.transform import Transformer
from pkg_resources import resource_filename

__all__ = ['UserQueriesModule']

class UserQueriesModule(Component):
    implements(ITemplateProvider, ITemplateStreamFilter)

    # ITemplateProvider methods
    def get_htdocs_dirs(self):
        return [('userqueries', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename(__name__, 'templates')]

    # ITemplateStreamFilter methods
    def filter_stream(self, req, method, filename, stream, formdata):
        if filename in ('query.html', 'report_view.html'):
            add_stylesheet(req, 'userqueries/css/userqueries.css')
            return stream | Transformer('//div[@id="content"]'). \
                                before(self._generate_form(req, formdata) ) \
                          | Transformer('//div[@class="buttons"]/form'). \
                                before(self._generate_button(req, formdata) ) \
                          | Transformer('//div[@id="ctxtnav"]//a[@href="/report"]').remove()
        return stream

    def _generate_button(self, req, data):
        userQueryData = dict(data)

        stream = Chrome(self.env).render_template(req, 'userqueries_button.html',
              userQueryData, fragment=True)
        return stream.select('//form')
    
    def _generate_form(self, req, data):
        userQueryData = dict(data)

        userQueryData['project_queries']=[]
        userQueryData['user_queries']   =[]

        userQueryData['empty_url']      = req.href.report()

        self.log.debug("Generating UserQueries navigation selector")

        # not really sure which is the best/definitive way yet:
        if userQueryData['report']:
            # SQL queries
            userQueryData['current_report_id'] = userQueryData['report']['id']
        elif userQueryData.has_key('report_resource'):
            # Custom queries in 0.11?
            userQueryData['current_report_id'] = int(userQueryData['report_resource'].id)
        elif userQueryData.has_key('context') and userQueryData['context'].req.args.has_key('report'):
            # Custom queries in 0.12?            
            userQueryData['current_report_id'] = int(userQueryData['context'].req.args['report'])
        else:
            # User visiting /report
            userQueryData['current_report_id'] = -1

        self.log.debug("User is visiting report %d", userQueryData['current_report_id'])

        db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute("SELECT id AS report, title FROM report ORDER BY report")
        for id, title in cursor:
            userQueryData['project_queries'].append({'url': req.href.report(id),
                                                     'id': id,
                                                     'name': title})

        stream = Chrome(self.env).render_template(req, 'userqueries.html',
              userQueryData, fragment=True)
        return stream.select('//form')
