import datetime

from c2corg_api.models.association import Association
from c2corg_api.models.document import (
    Document, DocumentLocale, DocumentGeometry, ArchiveDocument,
    ArchiveDocumentLocale, ArchiveDocumentGeometry)
from c2corg_api.models.document_history import DocumentVersion
from c2corg_api.models.feed import update_feed_document_create
from c2corg_api.models.outing import (
    Outing, OutingLocale, ArchiveOuting, ArchiveOutingLocale)
from c2corg_api.models.route import (
    Route, RouteLocale, ArchiveRoute, ArchiveRouteLocale)
from c2corg_api.models.waypoint import (
    Waypoint, WaypointLocale, ArchiveWaypoint, ArchiveWaypointLocale)
from c2corg_api.views.document import DocumentRest
from c2corg_api.tests.views import BaseTestRest


class TestDocumentDeleteRest(BaseTestRest):

    def setUp(self):  # noqa
        super(TestDocumentDeleteRest, self).setUp()
        self._prefix = '/documents/delete/'

        user_id = self.global_userids['contributor']

        self.waypoint1 = Waypoint(
            waypoint_type='summit', elevation=2000,
            geometry=DocumentGeometry(
                geom='SRID=3857;POINT(635956 5723604)'),
            locales=[
                WaypointLocale(
                    lang='fr', title='Dent de Crolles',
                    description='...',
                    summary='La Dent de Crolles')
            ])
        self.session.add(self.waypoint1)

        self.waypoint2 = Waypoint(
            waypoint_type='summit', elevation=4985,
            geometry=DocumentGeometry(
                geom='SRID=3857;POINT(635956 5723604)'),
            locales=[
                WaypointLocale(
                    lang='en', title='Mont Blanc',
                    description='...',
                    summary='The heighest point in Europe')
            ])
        self.session.add(self.waypoint2)

        self.waypoint3 = Waypoint(
            waypoint_type='summit', elevation=3,
            geometry=DocumentGeometry(
                geom='SRID=3857;POINT(635956 5723604)'))
        self.waypoint3.locales.append(WaypointLocale(
            lang='en', title='Mont Granier', description='...',
            access='yep'))
        self.waypoint3.locales.append(WaypointLocale(
            lang='fr', title='Mont Granier', description='...',
            access='ouai'))
        self.session.add(self.waypoint3)
        self.session.flush()

        DocumentRest.create_new_version(self.waypoint1, user_id)
        update_feed_document_create(self.waypoint1, user_id)
        DocumentRest.create_new_version(self.waypoint2, user_id)
        update_feed_document_create(self.waypoint2, user_id)
        DocumentRest.create_new_version(self.waypoint3, user_id)
        update_feed_document_create(self.waypoint3, user_id)
        self.session.flush()

        route1_geometry = DocumentGeometry(
            geom_detail='SRID=3857;LINESTRING(635956 5723604, 635966 5723644)',
            geom='SRID=3857;POINT(635961 5723624)')
        self.route1 = Route(
            activities=['skitouring'], elevation_max=1500, elevation_min=700,
            height_diff_up=800, height_diff_down=800, durations='1',
            main_waypoint_id=self.waypoint1.document_id,
            geometry=route1_geometry
        )
        self.route1.locales.append(RouteLocale(
            lang='en', title='Mont Blanc from the air', description='...',
            title_prefix='Mont Blanc :', gear='paraglider'))
        self.session.add(self.route1)

        route2_geometry = DocumentGeometry(
            geom_detail='SRID=3857;LINESTRING(635956 5723604, 635966 5723644)',
            geom='SRID=3857;POINT(635961 5723624)')
        self.route2 = Route(
            activities=['skitouring'], elevation_max=1500, elevation_min=700,
            height_diff_up=800, height_diff_down=800, durations='1',
            geometry=route2_geometry
        )
        self.route2.locales.append(RouteLocale(
            lang='en', title='Mont Blanc from the air', description='...',
            title_prefix='Mont Blanc :', gear='paraglider'))
        self.session.add(self.route2)
        self.session.flush()

        self.session.add(Association.create(
            parent_document=self.waypoint1,
            child_document=self.route1))
        self.session.add(Association.create(
            parent_document=self.waypoint2,
            child_document=self.route2))
        self.session.flush()

        route3_geometry = DocumentGeometry(
            geom_detail='SRID=3857;LINESTRING(635956 5723604, 635966 5723644)',
            geom='SRID=3857;POINT(635961 5723624)')
        self.route3 = Route(
            activities=['skitouring'], elevation_max=1500, elevation_min=700,
            height_diff_up=800, height_diff_down=800, durations='1',
            geometry=route3_geometry
        )
        self.route3.locales.append(RouteLocale(
            lang='en', title='Mont Blanc from the air', description='...',
            title_prefix='Mont Blanc :', gear='paraglider'))
        self.session.add(self.route3)
        self.session.flush()

        DocumentRest.create_new_version(self.route1, user_id)
        update_feed_document_create(self.route1, user_id)
        DocumentRest.create_new_version(self.route2, user_id)
        update_feed_document_create(self.route2, user_id)
        DocumentRest.create_new_version(self.route3, user_id)
        update_feed_document_create(self.route3, user_id)

        self.session.add(Association.create(
            parent_document=self.waypoint1,
            child_document=self.route3))
        self.session.add(Association.create(
            parent_document=self.waypoint2,
            child_document=self.route3))
        self.session.add(Association.create(
            parent_document=self.waypoint3,
            child_document=self.route3))
        self.session.flush()

        outing1_geometry = DocumentGeometry(
            geom_detail='SRID=3857;LINESTRING(635956 5723604, 635966 5723644)',
            geom='SRID=3857;POINT(635961 5723624)')
        self.outing1 = Outing(
            activities=['skitouring'], date_start=datetime.date(2016, 1, 1),
            date_end=datetime.date(2016, 1, 1),
            geometry=outing1_geometry,
            locales=[
                OutingLocale(
                    lang='en', title='...', description='...',
                    weather='sunny')
            ]
        )
        self.session.add(self.outing1)
        self.session.flush()

        DocumentRest.create_new_version(self.outing1, user_id)
        update_feed_document_create(self.outing1, user_id)
        self.session.add(Association.create(
            parent_document=self.route1,
            child_document=self.outing1))
        self.session.flush()

        outing2_geometry = DocumentGeometry(
            geom_detail='SRID=3857;LINESTRING(635956 5723604, 635966 5723644)',
            geom='SRID=3857;POINT(635961 5723624)')
        self.outing2 = Outing(
            activities=['skitouring'], date_start=datetime.date(2016, 1, 1),
            date_end=datetime.date(2016, 1, 1),
            geometry=outing2_geometry,
            locales=[
                OutingLocale(
                    lang='en', title='...', description='...',
                    weather='sunny')
            ]
        )
        self.session.add(self.outing2)
        self.session.flush()

        DocumentRest.create_new_version(self.outing2, user_id)
        update_feed_document_create(self.outing2, user_id)
        self.session.add(Association.create(
            parent_document=self.route2,
            child_document=self.outing2))
        self.session.add(Association.create(
            parent_document=self.route3,
            child_document=self.outing2))
        self.session.flush()

    def _delete(self, document_id, expected_status):
        headers = self.add_authorization_header(username='moderator')
        return self.app.delete_json(
            self._prefix + str(document_id),
            headers=headers, status=expected_status)

    def test_non_unauthorized(self):
        self.app.delete_json(
            self._prefix + str(self.waypoint1.document_id), {}, status=403)

        headers = self.add_authorization_header(username='contributor')
        return self.app.delete_json(
            self._prefix + str(self.waypoint1.document_id), {},
            headers=headers, status=403)

    def test_non_existing_document(self):
        self._delete(-9999999, 400)

    def test_delete_main_waypoint(self):
        """ Test that a main waypoint cannot be deleted.
        """
        response = self._delete(self.waypoint1.document_id, 400)
        errors = response.json.get('errors')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get('name'), 'Bad Request')
        self.assertEqual(
            errors[0].get('description'),
            'This waypoint cannot be deleted because it is a main waypoint.')

    def test_delete_only_waypoint_of_route(self):
        """ Test that the only waypoint of a route cannot be deleted.
        """
        response = self._delete(self.waypoint2.document_id, 400)
        errors = response.json.get('errors')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get('name'), 'Bad Request')
        self.assertEqual(
            errors[0].get('description'),
            'This waypoint cannot be deleted because '
            'it is the only waypoint associated to some routes.')

    def test_delete_only_route_of_outing(self):
        """ Test that a route cannot be deleted if it is the only route
            of some outing."""
        response = self._delete(self.route1.document_id, 400)
        errors = response.json.get('errors')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get('name'), 'Bad Request')
        self.assertEqual(
            errors[0].get('description'),
            'This route cannot be deleted because '
            'it is the only route associated to some outings.')

    def _test_delete(
            self, document_id, clazz, clazz_locale, archive_clazz,
            archive_clazz_locale):

        # Get the number of documents before deleting
        initial_count = self.session.query(clazz).count()
        initial_doc_count = self.session.query(Document).count()

        self._delete(document_id, 200)

        # Check that only one document has been deleted
        count = self.session.query(clazz).count()
        self.assertEqual(count, initial_count - 1)
        count = self.session.query(Document).count()
        self.assertEqual(count, initial_doc_count - 1)

        # Check that the document versions table is cleared
        count = self.session.query(DocumentVersion). \
            filter(DocumentVersion.document_id == document_id).count()
        self.assertEqual(0, count)

        # Check that entries have been removed in the main tables
        count = self.session.query(clazz). \
            filter(getattr(clazz, 'document_id') == document_id).count()
        self.assertEqual(0, count)
        count = self.session.query(Document). \
            filter(Document.document_id == document_id).count()
        self.assertEqual(0, count)
        if clazz_locale:
            count = self.session.query(clazz_locale). \
                filter(getattr(clazz_locale, 'document_id') == document_id). \
                count()
            self.assertEqual(0, count)
        count = self.session.query(DocumentLocale). \
            filter(DocumentLocale.document_id == document_id).count()
        self.assertEqual(0, count)
        count = self.session.query(DocumentGeometry). \
            filter(DocumentGeometry.document_id == document_id).count()
        self.assertEqual(0, count)

        # Check the archives have been cleared too
        count = self.session.query(archive_clazz). \
            filter(getattr(archive_clazz, 'document_id') == document_id). \
            count()
        self.assertEqual(0, count)
        count = self.session.query(ArchiveDocument). \
            filter(ArchiveDocument.document_id == document_id).count()
        self.assertEqual(0, count)
        if archive_clazz_locale:
            count = self.session.query(archive_clazz_locale). \
                filter(getattr(
                    archive_clazz_locale, 'document_id') == document_id). \
                count()
            self.assertEqual(0, count)
        count = self.session.query(ArchiveDocumentLocale). \
            filter(ArchiveDocumentLocale.document_id == document_id).count()
        self.assertEqual(0, count)
        count = self.session.query(ArchiveDocumentGeometry). \
            filter(ArchiveDocumentGeometry.document_id == document_id).count()
        self.assertEqual(0, count)

        # TODO check associations have been cleared
        # TODO check cache_versions have been updated
        # TODO check the feed has been cleared
        # TODO check comments have been cleared

    def test_delete_waypoint(self):
        self._test_delete(
            self.waypoint3.document_id,
            Waypoint, WaypointLocale, ArchiveWaypoint, ArchiveWaypointLocale)

    def test_delete_route(self):
        self._test_delete(
            self.route3.document_id,
            Route, RouteLocale, ArchiveRoute, ArchiveRouteLocale)

    def test_delete_outing(self):
        self._test_delete(
            self.outing1.document_id,
            Outing, OutingLocale, ArchiveOuting, ArchiveOutingLocale)

    def test_delete_outing_route_waypoint(self):
        self._test_delete(
            self.outing2.document_id,
            Outing, OutingLocale, ArchiveOuting, ArchiveOutingLocale)
        self._test_delete(
            self.route2.document_id,
            Route, RouteLocale, ArchiveRoute, ArchiveRouteLocale)
        self._test_delete(
            self.waypoint2.document_id,
            Waypoint, WaypointLocale, ArchiveWaypoint, ArchiveWaypointLocale)
