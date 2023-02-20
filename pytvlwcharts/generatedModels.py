# -*- coding: utf-8 -*-
"""
    generatedModels.py
    An Experimental Python Wrapper For Tradingview's Lightweight-Charts To Be Used In Notebook Environments.
    Generated With generateTypes.py. DO NOT MODIFY
    :url: https://tradingview.github.io/lightweight-charts/
    :copyright: (c) 2021 by Techfane Technologies Pvt. Ltd.
    :license: see LICENSE for details.
    :author: Dr June Moone
    :created: On Friday September 02, 2022 19:47:13 GMT+05:30
"""
__author__ = "Dr June Moone"
__webpage__ = "https://github.com/MooneDrJune"
__github__ = "https://github.com/TechfaneTechnologies/PyTvLwCharts"
__license__ = "MIT"

from apischema import alias
from apischema import serialize
from dataclasses import field
from dataclasses import dataclass
import enum
import json
from typing import Any, Optional, Union

class JsonOptions:
  def to_json(self):
    return json.dumps(serialize(self, exclude_none=True), indent=2)

@dataclass
class AxisPressedMouseMoveOptions(JsonOptions):
  """Represents options for how the time and price axes react to mouse movements.

  Attributes:
    price: Enable scaling the price axis by holding down the left mouse button and moving the mouse.
    time: Enable scaling the time axis by holding down the left mouse button and moving the mouse.
  """
  price: Optional[bool] = None
  time: Optional[bool] = None


class ColorType(enum.Enum):
  """ColorType"""

  # Solid color
  solid = 'solid'

  # Vertical gradient color
  vertical_gradient = 'gradient'


@dataclass
class SolidColor(JsonOptions):
  """Represents a solid color.

  Attributes:
    color: Color.
    type: Type of color.
  """
  color: Optional[str] = None
  type: ColorType = ColorType.solid


@dataclass
class VerticalGradientColor(JsonOptions):
  """Represents a vertical gradient of two colors.

  Attributes:
    bottom_color: Bottom color
    top_color: Top color
    type: Type of color.
  """
  bottom_color: Optional[str] = field(default=None, metadata=alias('bottomColor'))
  top_color: Optional[str] = field(default=None, metadata=alias('topColor'))
  type: ColorType = ColorType.vertical_gradient


# Represents the background color of the chart.
Background = Union[SolidColor, VerticalGradientColor]


class LineStyle(enum.IntEnum):
  """Represents the possible line styles."""

  LINESTYLE_0 = 0
  LINESTYLE_1 = 1
  LINESTYLE_2 = 2
  LINESTYLE_3 = 3
  LINESTYLE_4 = 4


class LineWidth(enum.IntEnum):
  """Represents the width of a line."""

  LINEWIDTH_1 = 1
  LINEWIDTH_2 = 2
  LINEWIDTH_3 = 3
  LINEWIDTH_4 = 4


@dataclass
class CrosshairLineOptions(JsonOptions):
  """Structure describing a crosshair line (vertical or horizontal)

  Attributes:
    color: Crosshair line color.
    label_background_color: Crosshair label background color.
    label_visible: Display the crosshair label on the relevant scale.
    style: Crosshair line style.
    visible: Display the crosshair line.
    width: Crosshair line width.
  """
  color: Optional[str] = None
  label_background_color: Optional[str] = field(default=None, metadata=alias('labelBackgroundColor'))
  label_visible: Optional[bool] = field(default=None, metadata=alias('labelVisible'))
  style: Optional[LineStyle] = None
  visible: Optional[bool] = None
  width: Optional[LineWidth] = None


class CrosshairMode(enum.IntEnum):
  """Represents the crosshair mode."""

  CROSSHAIRMODE_0 = 0
  CROSSHAIRMODE_1 = 1


@dataclass
class CrosshairOptions(JsonOptions):
  """Structure describing crosshair options

  Attributes:
    horz_line: Horizontal line options.
    mode: Crosshair mode
    vert_line: Vertical line options.
  """
  horz_line: Optional[CrosshairLineOptions] = field(default=None, metadata=alias('horzLine'))
  mode: Optional[CrosshairMode] = None
  vert_line: Optional[CrosshairLineOptions] = field(default=None, metadata=alias('vertLine'))


@dataclass
class GridLineOptions(JsonOptions):
  """Grid line options.

  Attributes:
    color: Line color.
    style: Line style.
    visible: Display the lines.
  """
  color: Optional[str] = None
  style: Optional[LineStyle] = None
  visible: Optional[bool] = None


@dataclass
class GridOptions(JsonOptions):
  """Structure describing grid options.

  Attributes:
    horz_lines: Horizontal grid line options.
    vert_lines: Vertical grid line options.
  """
  horz_lines: Optional[GridLineOptions] = field(default=None, metadata=alias('horzLines'))
  vert_lines: Optional[GridLineOptions] = field(default=None, metadata=alias('vertLines'))


@dataclass
class HandleScaleOptions(JsonOptions):
  """Represents options for how the chart is scaled by the mouse and touch gestures.

  Attributes:
    axis_double_click_reset: Enable resetting scaling by double-clicking the left mouse button.
    axis_pressed_mouse_move: Enable scaling the price and/or time scales by holding down the left mouse button and moving the mouse.
    mouse_wheel: Enable scaling with the mouse wheel.
    pinch: Enable scaling with pinch/zoom gestures.
  """
  axis_double_click_reset: Optional[bool] = field(default=None, metadata=alias('axisDoubleClickReset'))
  axis_pressed_mouse_move: Optional[Union[AxisPressedMouseMoveOptions, bool]] = field(default=None, metadata=alias('axisPressedMouseMove'))
  mouse_wheel: Optional[bool] = field(default=None, metadata=alias('mouseWheel'))
  pinch: Optional[bool] = None


@dataclass
class HandleScrollOptions(JsonOptions):
  """Represents options for how the chart is scrolled by the mouse and touch gestures.

  Attributes:
    horz_touch_drag: Enable horizontal touch scrolling. When enabled the chart handles touch gestures that would normally scroll the webpage horizontally.
    mouse_wheel: Enable scrolling with the mouse wheel.
    pressed_mouse_move: Enable scrolling by holding down the left mouse button and moving the mouse.
    vert_touch_drag: Enable vertical touch scrolling. When enabled the chart handles touch gestures that would normally scroll the webpage vertically.
  """
  horz_touch_drag: Optional[bool] = field(default=None, metadata=alias('horzTouchDrag'))
  mouse_wheel: Optional[bool] = field(default=None, metadata=alias('mouseWheel'))
  pressed_mouse_move: Optional[bool] = field(default=None, metadata=alias('pressedMouseMove'))
  vert_touch_drag: Optional[bool] = field(default=None, metadata=alias('vertTouchDrag'))


class HorzAlign(enum.Enum):
  """Represents a horizontal alignment."""

  center = 'center'
  left = 'left'
  right = 'right'


@dataclass
class KineticScrollOptions(JsonOptions):
  """Represents options for enabling or disabling kinetic scrolling with mouse and touch gestures.

  Attributes:
    mouse: Enable kinetic scroll with the mouse.
    touch: Enable kinetic scroll with touch gestures.
  """
  mouse: Optional[bool] = None
  touch: Optional[bool] = None


@dataclass
class LayoutOptions(JsonOptions):
  """Represents layout options

  Attributes:
    background: Chart and scales background color.
    background_color:
    font_family: Font family of text on the scales.
    font_size: Font size of text on scales in pixels.
    text_color: Color of text on the scales.
  """
  background: Optional[Background] = None
  background_color: Optional[str] = field(default=None, metadata=alias('backgroundColor'))
  font_family: Optional[str] = field(default=None, metadata=alias('fontFamily'))
  font_size: Optional[int] = field(default=None, metadata=alias('fontSize'))
  text_color: Optional[str] = field(default=None, metadata=alias('textColor'))


# A function used to format a{@linkBarPrice}as a string.
__type_2 = Any


# PriceFormatterFn
PriceFormatterFn = __type_2


# A custom function used to override formatting of a time to a string.
__type_3 = Any


# TimeFormatterFn
TimeFormatterFn = __type_3


@dataclass
class LocalizationOptions(JsonOptions):
  """Represents options for formatting dates, times, and prices according to a locale.

  Attributes:
    date_format: Date formatting string. Can contain `yyyy`, `yy`, `MMMM`, `MMM`, `MM` and `dd` literals which will be replaced with corresponding date's value. Ignored if timeFormatter has been specified.
    locale: Current locale used to format dates. Uses the browser's language settings by default.
    price_formatter: Override formatting of the price scale crosshair label. Can be used for cases that can't be covered with built-in price formats.
    time_formatter: Override formatting of the time scale crosshair label.
  """
  date_format: Optional[str] = field(default=None, metadata=alias('dateFormat'))
  locale: Optional[str] = None
  price_formatter: Optional[PriceFormatterFn] = field(default=None, metadata=alias('priceFormatter'))
  time_formatter: Optional[TimeFormatterFn] = field(default=None, metadata=alias('timeFormatter'))


class PriceScaleMode(enum.IntEnum):
  """Represents the price scale mode."""

  PRICESCALEMODE_0 = 0
  PRICESCALEMODE_1 = 1
  PRICESCALEMODE_2 = 2
  PRICESCALEMODE_3 = 3


class PriceAxisPosition(enum.Enum):
  """Represents the position of a price axis relative to the chart."""

  left = 'left'
  none = 'none'
  right = 'right'


@dataclass
class PriceScaleMargins(JsonOptions):
  """Defines margins of the price scale.

  Attributes:
    bottom: Bottom margin in percentages. Must be greater or equal to 0 and less than 1.
    top: Top margin in percentages. Must be greater or equal to 0 and less than 1.
  """
  bottom: Optional[int] = None
  top: Optional[int] = None


@dataclass
class __type(JsonOptions):
  """Represents overlay price scale options.

  Attributes:
    align_labels: Align price scale labels to prevent them from overlapping.
    border_color: Price scale border color.
    border_visible: Set true to draw a border between the price scale and the chart area.
    draw_ticks: Draw small horizontal line on price axis labels.
    entire_text_only: Show top and bottom corner labels only if entire text is visible.
    invert_scale: Invert the price scale, so that a upwards trend is shown as a downwards trend and vice versa. Affects both the price scale and the data on the chart.
    mode: Price scale mode.
    position: Price scale's position on the chart.
    scale_margins: Price scale margins.
  """
  align_labels: Optional[bool] = field(default=None, metadata=alias('alignLabels'))
  border_color: Optional[str] = field(default=None, metadata=alias('borderColor'))
  border_visible: Optional[bool] = field(default=None, metadata=alias('borderVisible'))
  draw_ticks: Optional[bool] = field(default=None, metadata=alias('drawTicks'))
  entire_text_only: Optional[bool] = field(default=None, metadata=alias('entireTextOnly'))
  invert_scale: Optional[bool] = field(default=None, metadata=alias('invertScale'))
  mode: Optional[PriceScaleMode] = None
  position: Optional[PriceAxisPosition] = None
  scale_margins: Optional[PriceScaleMargins] = field(default=None, metadata=alias('scaleMargins'))


# OverlayPriceScaleOptions
OverlayPriceScaleOptions = __type


@dataclass
class PriceScaleOptions(JsonOptions):
  """Structure that describes price scale options

  Attributes:
    align_labels: Align price scale labels to prevent them from overlapping.
    auto_scale: Automatically set price range based on visible data range.
    border_color: Price scale border color.
    border_visible: Set true to draw a border between the price scale and the chart area.
    draw_ticks: Draw small horizontal line on price axis labels.
    entire_text_only: Show top and bottom corner labels only if entire text is visible.
    invert_scale: Invert the price scale, so that a upwards trend is shown as a downwards trend and vice versa. Affects both the price scale and the data on the chart.
    mode: Price scale mode.
    position: Price scale's position on the chart.
    scale_margins: Price scale margins.
    visible: Indicates if this price scale visible. Ignored by overlay price scales.
  """
  align_labels: Optional[bool] = field(default=None, metadata=alias('alignLabels'))
  auto_scale: Optional[bool] = field(default=None, metadata=alias('autoScale'))
  border_color: Optional[str] = field(default=None, metadata=alias('borderColor'))
  border_visible: Optional[bool] = field(default=None, metadata=alias('borderVisible'))
  draw_ticks: Optional[bool] = field(default=None, metadata=alias('drawTicks'))
  entire_text_only: Optional[bool] = field(default=None, metadata=alias('entireTextOnly'))
  invert_scale: Optional[bool] = field(default=None, metadata=alias('invertScale'))
  mode: Optional[PriceScaleMode] = None
  position: Optional[PriceAxisPosition] = None
  scale_margins: Optional[PriceScaleMargins] = field(default=None, metadata=alias('scaleMargins'))
  visible: Optional[bool] = None


# The `TickMarkFormatter` is used to customize tick mark labels on the time scale. This function should return `time` as a string formatted according to `tickMarkType` type (year, month, etc) and `locale`. Note that the returned string should be the shortest possible value and should have no more than 8 characters. Otherwise, the tick marks will overlap each other.
__type_1 = Any


# TickMarkFormatter
TickMarkFormatter = __type_1


@dataclass
class TimeScaleOptions(JsonOptions):
  """Options for the time scale; the horizontal scale at the bottom of the chart that displays the time of data.

  Attributes:
    bar_spacing: The space between bars in pixels.
    border_color: The time scale border color.
    border_visible: Show the time scale border.
    fix_left_edge: Prevent scrolling to the left of the first bar.
    fix_right_edge: Prevent scrolling to the right of the most recent bar.
    lock_visible_time_range_on_resize: Prevent changing the visible time range during chart resizing.
    min_bar_spacing: The minimum space between bars in pixels.
    right_bar_stays_on_scroll: Prevent the hovered bar from moving when scrolling.
    right_offset: The margin space in bars from the right side of the chart.
    seconds_visible: Show seconds in the time scale and vertical crosshair label in `hh:mm:ss` format for intraday data.
    shift_visible_range_on_new_bar: Shift the visible range to the right (into the future) by the number of new bars when new data is added. Note that this only applies when the last bar is visible.
    tick_mark_formatter: Override the default tick marks formatter.
    time_visible: Show the time, not just the date, in the time scale and vertical crosshair label.
    visible: Show the time scale.
  """
  bar_spacing: Optional[int] = field(default=None, metadata=alias('barSpacing'))
  border_color: Optional[str] = field(default=None, metadata=alias('borderColor'))
  border_visible: Optional[bool] = field(default=None, metadata=alias('borderVisible'))
  fix_left_edge: Optional[bool] = field(default=None, metadata=alias('fixLeftEdge'))
  fix_right_edge: Optional[bool] = field(default=None, metadata=alias('fixRightEdge'))
  lock_visible_time_range_on_resize: Optional[bool] = field(default=None, metadata=alias('lockVisibleTimeRangeOnResize'))
  min_bar_spacing: Optional[int] = field(default=None, metadata=alias('minBarSpacing'))
  right_bar_stays_on_scroll: Optional[bool] = field(default=None, metadata=alias('rightBarStaysOnScroll'))
  right_offset: Optional[int] = field(default=None, metadata=alias('rightOffset'))
  seconds_visible: Optional[bool] = field(default=None, metadata=alias('secondsVisible'))
  shift_visible_range_on_new_bar: Optional[bool] = field(default=None, metadata=alias('shiftVisibleRangeOnNewBar'))
  tick_mark_formatter: Optional[TickMarkFormatter] = field(default=None, metadata=alias('tickMarkFormatter'))
  time_visible: Optional[bool] = field(default=None, metadata=alias('timeVisible'))
  visible: Optional[bool] = None


class VertAlign(enum.Enum):
  """Represents a vertical alignment."""

  bottom = 'bottom'
  center = 'center'
  top = 'top'


# Structure that describes price scale options
VisiblePriceScaleOptions = PriceScaleOptions


@dataclass
class WatermarkOptions(JsonOptions):
  """Watermark options.

  Attributes:
    color: Watermark color.
    font_family: Font family.
    font_size: Font size in pixels.
    font_style: Font style.
    horz_align: Horizontal alignment inside the chart area.
    text: Text of the watermark. Word wrapping is not supported.
    vert_align: Vertical alignment inside the chart area.
    visible: Display the watermark.
  """
  color: Optional[str] = None
  font_family: Optional[str] = field(default=None, metadata=alias('fontFamily'))
  font_size: Optional[int] = field(default=None, metadata=alias('fontSize'))
  font_style: Optional[str] = field(default=None, metadata=alias('fontStyle'))
  horz_align: Optional[HorzAlign] = field(default=None, metadata=alias('horzAlign'))
  text: Optional[str] = None
  vert_align: Optional[VertAlign] = field(default=None, metadata=alias('vertAlign'))
  visible: Optional[bool] = None


@dataclass
class ChartOptions(JsonOptions):
  """Structure describing options of the chart. Series options are to be set separately

  Attributes:
    crosshair: Crosshair options
    grid: Grid options.
    handle_scale: Scale options, or a boolean flag that enables/disables scaling
    handle_scroll: Scroll options, or a boolean flag that enables/disables scrolling
    height: Height of the chart in pixels
    kinetic_scroll: Kinetic scroll options
    layout: Layout options
    left_price_scale: Left price scale options
    localization: Localization options.
    overlay_price_scales: Overlay price scale options
    price_scale: Price scale options.
    right_price_scale: Right price scale options
    time_scale: Time scale options
    watermark: Watermark options. A watermark is a background label that includes a brief description of the drawn data. Any text can be added to it. Please make sure you enable it and set an appropriate font color and size to make your watermark visible in the background of the chart. We recommend a semi-transparent color and a large font. Also note that watermark position can be aligned vertically and horizontally.
    width: Width of the chart in pixels
  """
  crosshair: Optional[CrosshairOptions] = None
  grid: Optional[GridOptions] = None
  handle_scale: Optional[Union[HandleScaleOptions, bool]] = field(default=None, metadata=alias('handleScale'))
  handle_scroll: Optional[Union[HandleScrollOptions, bool]] = field(default=None, metadata=alias('handleScroll'))
  height: Optional[Union[int,float,str]] = None
  kinetic_scroll: Optional[KineticScrollOptions] = field(default=None, metadata=alias('kineticScroll'))
  layout: Optional[LayoutOptions] = None
  left_price_scale: Optional[VisiblePriceScaleOptions] = field(default=None, metadata=alias('leftPriceScale'))
  localization: Optional[LocalizationOptions] = None
  overlay_price_scales: Optional[OverlayPriceScaleOptions] = field(default=None, metadata=alias('overlayPriceScales'))
  price_scale: Optional[PriceScaleOptions] = field(default=None, metadata=alias('priceScale'))
  right_price_scale: Optional[VisiblePriceScaleOptions] = field(default=None, metadata=alias('rightPriceScale'))
  time_scale: Optional[TimeScaleOptions] = field(default=None, metadata=alias('timeScale'))
  watermark: Optional[WatermarkOptions] = None
  width: Optional[Union[int,float,str]] = None
