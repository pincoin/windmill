import logging


class PageableMixin(object):
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        block_size = 5

        context = super(PageableMixin, self).get_context_data(**kwargs)

        start_index = int((context['page_obj'].number - 1) / block_size) * block_size
        end_index = min(start_index + block_size, len(context['paginator'].page_range))

        context['page_range'] = context['paginator'].page_range[start_index:end_index]
        return context

    def get_paginate_by(self, queryset):
        chunk_size = 10
        return chunk_size
