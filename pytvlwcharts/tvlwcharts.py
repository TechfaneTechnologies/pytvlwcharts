# -*- coding: utf-8 -*-
"""
    tvlwcharts.py
    An Experimental Python Wrapper For Tradingview's Lightweight-Charts To Be Used In Notebook Environments.
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

from .generatedModels import *

import copy
import dataclasses
import itertools
import jinja2
import json
import pandas as pd
import uuid

from typing import Dict, Optional, List

_TEMPLATE = jinja2.Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0" />
    <title>Lightweight Charts Customization Tutorial</title>
    <!-- Adding Google Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet" />
    <!-- Adding the standalone version of Lightweight charts -->
    <script type="text/javascript" src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <script type="text/javascript" src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <style>
        body {
        padding: 0;
        margin: 0;
        /* Add a background color to match the chart */
        background-color: #222;
      }

      /* Styles for attribution message */
      .lw-attribution {
        position: absolute;
        left: 0px;
        top: 0px;
        z-index: 3; /* place above the charts */
        padding: 10px 0px 0px 12px;
        font-family: "Roboto", sans-serif;
        font-size: 0.8em;
      }
      .lw-attribution a {
        cursor: pointer;
        color: rgb(54, 116, 217);
        opacity: 0.8;
      }
      .lw-attribution a:hover {
        color: rgb(54, 116, 217);
        opacity: 1;
      }
    </style>
</head>
<body>
   <script src="{{ base_url }}lightweight-charts.standalone.production.js"></script> 
   <script type="text/javascript" src="https://unpkg.com/axios/dist/axios.min.js"></script>
   <div id="{{ output_div }}" style="position: absolute; width: 100%; height: 100%">
     <div class="lw-attribution">
       <a href="https://tradingview.github.io/lightweight-charts/">Made By DrJuneMoone</a>
     </div>
   </div>
   <script type="text/javascript">
     (() => {
     const outputDiv = document.getElementById("{{ output_div }}");
     const chart = LightweightCharts.createChart(outputDiv, {{ chart.options }});
     {% for series in chart.series %}
     (() => {
       const chart_series_{{ series.series_name }} = chart.add{{ series.series_type }}Series(
         {{ series.options }}
       );
       chart_series_{{ series.series_name }}.setData(
         {{ series.data }}
       );
       chart_series_{{ series.series_name }}.setMarkers(
         {{ series.markers }}
       );
       {% for price_line in series.price_lines %}
       chart_series_{{ series.series_name }}.createPriceLine({{ price_line }});
       {% endfor %}
       this.chart_series_{{ series.series_name }} = chart_series_{{ series.series_name }};
     })();
     {% endfor %}
      chart.timeScale().fitContent();
      chart.subscribeClick(function (param) {
        console.log(`An user clicks at (${param.point.x}, ${param.point.y}) point, the time is ${param.time}`);
      });
      chart.unsubscribeClick(function (param) {
        // Don’t get notified when a mouse clicks on a chart
      });
      chart.subscribeCrosshairMove(function (param) {
        if (!param.point) {
          return;
        }
        if (param.time) {
          const volume = param.seriesPrices.get(chart_series_volume)
          const ohlc = param.seriesPrices.get(chart_series_ohlc)
          const dateFormat = new Date(param.time * 1000)
          const dateFormats = dateFormat.getUTCDate() + "/" + (dateFormat.getUTCMonth() + 1) + "/" + dateFormat.getUTCFullYear() + " " + dateFormat.getUTCHours() + ":" + dateFormat.getUTCMinutes() + ":" + dateFormat.getUTCSeconds()
          document.getElementsByClassName('lw-attribution')[0].innerText = `Time: ${dateFormats} | Open: ${ohlc.open.toFixed(2)} | High: ${ohlc.high.toFixed(2)} | Low: ${ohlc.low.toFixed(2)} | Close: ${ohlc.close.toFixed(2)} | Volume: ${volume}`
        } else {
            console.log(`A user moved the crosshair to (${param.point.x}, ${param.point.y}) point, the time is ${param.time}`);
        }
      });
      // Make prices fully visible
      document.querySelector("#chart > div > table > tr:nth-child(1) > td:nth-child(3) > div").style["left"] = "-30px";
      // Make legend fully visible
      document.querySelector("#chart > div > table > tr:nth-child(1) > td:nth-child(2) > div").style["left"] = "-30px";
      window.addEventListener("resize", () => {
        chart.resize(window.innerWidth, window.innerHeight);
      });
     })();
   </script>
</body>
</html>
""")

_TEMPLATES = jinja2.Template("""
   <script type="text/javascript" src="https://unpkg.com/axios/dist/axios.min.js"></script>
   <script src="{{ base_url }}lightweight-charts.standalone.production.js"></script>
   <div id="{{ output_div }}"></div>
   <script type="text/javascript">
     (() => {
     const outputDiv = document.getElementById("{{ output_div }}");
     const chart = LightweightCharts.createChart(outputDiv, {{ chart.options }});
     {% for series in chart.series %}
     (() => {
       const chart_series_{{ series.series_name }} = chart.add{{ series.series_type }}Series(
         {{ series.options }}
       );
       chart_series_{{ series.series_name }}.setData(
         {{ series.data }}
       );
       chart_series_{{ series.series_name }}.setMarkers(
         {{ series.markers }}
       );
       {% for price_line in series.price_lines %}
       chart_series_{{ series.series_name }}.createPriceLine({{ price_line }});
       {% endfor %}
       this.chart_series_{{ series.series_name }} = chart_series_{{ series.series_name }};
     })();
     {% endfor %}
      chart.timeScale().fitContent();
      chart.subscribeClick(function (param) {
        console.log(`An user clicks at (${param.point.x}, ${param.point.y}) point, the time is ${param.time}`);
      });
      chart.unsubscribeClick(function (param) {
        // Don’t get notified when a mouse clicks on a chart
      });
      chart.subscribeCrosshairMove(function (param) {
        console.log(`A user moved the crosshair to (${param.point.x}, ${param.point.y}) point, the time is ${param.time}`);
      });
      // Make prices fully visible
      document.querySelector("#chart > div > table > tr:nth-child(1) > td:nth-child(3) > div").style["left"] = "-30px";
      // Make legend fully visible
      document.querySelector("#chart > div > table > tr:nth-child(1) > td:nth-child(2) > div").style["left"] = "-30px";
      window.addEventListener("resize", () => {
        chart.resize(window.innerWidth, window.innerHeight);
      });
     })();
   </script>
""")

# Initiate Model Specification.
@dataclasses.dataclass
class _SeriesSpec:
  series_name: str 
  series_type: str
  data: str
  options: str
  price_lines: List[Dict]
  markers: str


@dataclasses.dataclass
class _ChartSpec:
  options: str
  series: List[_SeriesSpec]


def _render(serve: bool,
            chart: _ChartSpec,
            base_url: str = "https://unpkg.com/lightweight-charts/dist/",
            output_div: str = "vis") -> str:
  """Render a model as html for viewing."""
  return (
      _TEMPLATE.render(chart=chart, base_url=base_url, output_div=output_div)
      if serve
      else _TEMPLATES.render(chart=chart, base_url=base_url, output_div=output_div)
  )


def _encode(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
  """Rename and select columns from a data frame."""
  return data.rename(columns={value: key for key, value in kwargs.items()})[[
      *kwargs.keys()
  ]]


class _Markers:
  """Series Markers."""

  def __init__(self, chart, data: pd.DataFrame, **kwargs):
    self._chart = chart
    self._data = data
    self.options = kwargs

  def encode(self, **kwargs):
    self._data = _encode(self._data, **kwargs)

  def _spec(self):
    return [{
        **self.options,
        **marker
    } for marker in self._data.to_dict(orient='records')]

  def _repr_html_(self):
    return self._chart._repr_html_()


class Series:

  def __init__(self, chart, data: pd.DataFrame, series_name: str, series_type: str, **kwargs):
    self._chart = chart
    self.series_name = series_name
    self.series_type = series_type
    self._data = data
    self.options = kwargs
    self._price_lines = []
    self._single_markers = []
    self._markers = []

  def encode(self, **kwargs):
    self._data = _encode(self._data, **kwargs)
    return self

  def price_line(self, **kwargs):
    self._price_lines.append(kwargs)
    return self

  def annotation(self, **kwargs):
    self._single_markers.append(kwargs)
    return self

  def mark_annotation(self, data: pd.DataFrame = None, **kwargs) -> _Markers:
    markers = _Markers(chart=self._chart,
                       data=data if data is not None else self._data,
                       **kwargs)
    self._markers.append(markers)
    return markers

  def _spec(self) -> _SeriesSpec:
    return _SeriesSpec(
        series_name=self.series_name,
        series_type=self.series_type,
        data=self._data.to_json(orient='records', date_format='iso'),
        options=json.dumps(self.options),
        price_lines=self._price_lines,
        markers=json.dumps(self._single_markers + list(
            itertools.chain(*[marker._spec() for marker in self._markers]))))

  def _repr_html_(self):
    return self._chart._repr_html_()


class Chart:
  """A Lightweight Chart."""

  def __init__(self,
               serve: bool = False,
               data: pd.DataFrame = None,
               width: int = 400,
               height: int = 300,
               crosshair: Optional[CrosshairOptions] = None,
               grid: Optional[GridOptions] = None,
               handle_scale: Optional[Union[HandleScaleOptions, bool]] = None,
               handle_scroll: Optional[Union[HandleScrollOptions, bool]] = None,
               kinetic_scroll: Optional[KineticScrollOptions] = None,
               layout: Optional[LayoutOptions] = None,
               left_price_scale: Optional[VisiblePriceScaleOptions] = None,
               localization: Optional[LocalizationOptions] = None,
               overlay_price_scales: Optional[OverlayPriceScaleOptions] = None,
               price_scale: Optional[PriceScaleOptions] = None,
               right_price_scale: Optional[VisiblePriceScaleOptions] = None,
               time_scale: Optional[TimeScaleOptions] = None,
               watermark: Optional[WatermarkOptions] = None,
               options: Optional[ChartOptions] = None):
    self.options = copy.deepcopy(options) if options else ChartOptions()
    self.series = []
    self._data = data.drop_duplicates(subset=['time']) if data is not None else data
    self.serve = serve
    # Set Options Overrides.
    self.options.width = width
    self.options.height = height
    if crosshair:
      self.options.crosshair = copy.deepcopy(crosshair)
    if grid:
      self.options.grid = copy.deepcopy(grid)
    if handle_scale:
      self.options.handle_scale = copy.deepcopy(handle_scale)
    if handle_scroll:
      self.options.handle_scale = copy.deepcopy(handle_scroll)
    if kinetic_scroll:
      self.options.kinetic_scroll = copy.deepcopy(kinetic_scroll)
    if layout:
      self.options.layout = copy.deepcopy(layout)
    if left_price_scale:
      self.options.left_price_scale = copy.deepcopy(left_price_scale)
    if localization:
      self.options.localization = copy.deepcopy(localization)
    if overlay_price_scales:
      self.options.overlay_price_scales = copy.deepcopy(overlay_price_scales)
    if price_scale:
      self.options.price_scale = copy.deepcopy(price_scale)
    if right_price_scale:
      self.options.right_price_scale = copy.deepcopy(right_price_scale)
    if time_scale:
      self.options.time_scale = copy.deepcopy(time_scale)
    if watermark:
      self.options.watermark = copy.deepcopy(watermark)

  def add(self, series: Series):
    self.series.append(series)
    return series

  def mark_line(self, series_name:str = None, data: pd.DataFrame = None, **kwargs) -> Series:
    """Add A Line Series."""
    return self.add(
        Series(chart=self,
               series_name=series_name,
               series_type='Line',
               data=data.drop_duplicates(subset=['time']) if data is not None else self._data,
               **kwargs))

  def mark_area(self, series_name:str = None, data: pd.DataFrame = None, **kwargs) -> Series:
    """Add An Area Series."""
    return self.add(
        Series(chart=self,
               series_name=series_name,
               series_type='Area',
               data=data.drop_duplicates(subset=['time']) if data is not None else self._data,
               **kwargs))

  def mark_bar(self, series_name:str = None, data: pd.DataFrame = None, **kwargs) -> Series:
    """Add A Bar Series."""
    return self.add(
        Series(chart=self,
               series_name=series_name,
               series_type='Bar',
               data=data.drop_duplicates(subset=['time']) if data is not None else self._data,
               **kwargs))

  def mark_candlestick(self, series_name:str = None, data: pd.DataFrame = None, **kwargs) -> Series:
    """Add A Candlestick series."""
    return self.add(
        Series(chart=self,
               series_name=series_name,
               series_type='Candlestick',
               data=data.drop_duplicates(subset=['time']) if data is not None else self._data,
               **kwargs))

  def mark_histogram(self, series_name:str = None, data: pd.DataFrame = None, **kwargs) -> Series:
    """Add A Histogram Series."""
    return self.add(
        Series(chart=self,
               series_name=series_name,
               series_type='Histogram',
               data=data.drop_duplicates(subset=['time']) if data is not None else self._data,
               **kwargs))

  def _spec(self) -> _ChartSpec:
    return _ChartSpec(options=self.options.to_json(),
                      series=[series._spec() for series in self.series])

  def _repr_html_(self):
    return _render(self.serve, self._spec(), output_div=f'vis-{uuid.uuid4().hex}')
