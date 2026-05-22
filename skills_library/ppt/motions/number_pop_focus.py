"""Number Pop Focus — A fast pop-in zoom that makes a large number feel newly surfaced and important.

Distilled from Animista
Source: https://animista.net/
"""
from __future__ import annotations

ORIGIN = "web_distilled"
SOURCE_URL = 'https://animista.net/'
SOURCE_TITLE = 'Animista'

NAME = 'number_pop_focus'
CATEGORY = 'emphasis'
DESCRIPTION = 'A fast pop-in zoom that makes a large number feel newly surfaced and important.'
APPLICABILITY = {'roles': ['headline number', 'stat reveal', 'hero metric'], 'anchor_names': ['metric_xl', 'value', 'title', 'title_xl', 'hero_headline'], 'max_per_slide': 2}
PARAMETERS = {'delay_ms': {'type': 'int', 'default': 0, 'min': 0, 'max': 3000}, 'duration_ms': {'type': 'int', 'default': 260, 'min': 140, 'max': 800}}

TAGS = ['number', 'zoom', 'pop', 'stat', 'focus']
INTENSITY = 7
MOOD = ['bold', 'punchy', 'boardroom']
ARCHETYPE_FIT = ['data', 'boardroom', 'narrative']
EMBEDDING_TEXT = 'Apply to a large numeral or short value when you need a crisp attention-grab. It works well for revenue, growth, savings, and market-share callouts.'
CONTENT_MATCHERS = {}
COMPLEMENTARY_WITH = ['count_up_metric', 'headline_word_cascade', 'chart_peak_ping']
CONFLICTS_WITH = ['dramatic_zoom', 'metric_snap_pop', 'bounce_in']


def apply(slide, target_shape, params=None):
    from _motion_helpers import emit_zoom_in
    p = dict(params or {})
    emit_zoom_in(slide, target_shape, p.get('delay_ms', 0), p.get('duration_ms', 260))
