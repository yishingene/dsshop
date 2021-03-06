from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class OrdersDashboardApplication(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]
    permissions_map = {
        'order-list': (['is_staff'], ['partner.dashboard_access']),
        'order-stats': (['is_staff'], ['partner.dashboard_access']),
        'order-detail': (['is_staff'], ['partner.dashboard_access']),
        'order-detail-note': (['is_staff'], ['partner.dashboard_access']),
        'order-line-detail': (['is_staff'], ['partner.dashboard_access']),
        'order-shipping-address': (['is_staff'], ['partner.dashboard_access']),
        'order-invoice': (['is_staff'], ['is_active'], ['partner.dashboard_access']),
        'order-invoice-download': (['is_staff'], ['is_active'], ['partner.dashboard_access']),
    }

    order_list_view = get_class('dashboard.orders.views', 'OrderListView')
    order_detail_view = get_class('dashboard.orders.views', 'OrderDetailView')
    shipping_address_view = get_class('dashboard.orders.views',
                                      'ShippingAddressUpdateView')
    line_detail_view = get_class('dashboard.orders.views', 'LineDetailView')
    order_stats_view = get_class('dashboard.orders.views', 'OrderStatsView')
    order_invoice_view = get_class('dashboard.orders.views', 'InvoicePdfView')
    order_invoice_download_view = get_class('dashboard.orders.views', 'InvoiceDownloadView')

    def get_urls(self):
        urls = [
            url(r'^$', self.order_list_view.as_view(), name='order-list'),
            url(r'^statistics/$', self.order_stats_view.as_view(),
                name='order-stats'),
            url(r'^(?P<number>[-\w]+)/$',
                self.order_detail_view.as_view(), name='order-detail'),
            url(r'^(?P<number>[-\w]+)/notes/(?P<note_id>\d+)/$',
                self.order_detail_view.as_view(), name='order-detail-note'),
            url(r'^(?P<number>[-\w]+)/lines/(?P<line_id>\d+)/$',
                self.line_detail_view.as_view(), name='order-line-detail'),
            url(r'^(?P<number>[-\w]+)/shipping-address/$',
                self.shipping_address_view.as_view(),
                name='order-shipping-address'),
            url(r'^invoice/(?P<number>[-\w]+)/$',
                self.order_invoice_view.as_view(), name='order-invoice'),
            url(r'^invoice/(?P<number>[-\w]+)/download/$',
                self.order_invoice_download_view.as_view(), name='order-invoice-download')
        ]
        return self.post_process_urls(urls)


application = OrdersDashboardApplication()