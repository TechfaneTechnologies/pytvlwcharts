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
    </style>
</head>
<body>
   <div id="{{ output_div }}" style="position: absolute; width: 100%; height: 100%"></div>
   <script type="text/javascript">
     (() => {
     const outputDiv = document.getElementById("{{ output_div }}");
     const chart = LightweightCharts.createChart(outputDiv, {{ chart.options }});
     this.chart = chart;
     const container = document.getElementById("{{ output_div }}");
     const legend = document.createElement('div');
     legend.style = `position: absolute; left: 10px; top: 10px; z-index: 1; font-size: 10px; font-family: sans-serif; line-height: 14px; font-weight: 200;`;
     container.appendChild(legend);
     {% for series in chart.series %}
     (() => {
       const row_{{ series.series_name }} = document.createElement('div');
       row_{{ series.series_name }}.innerHTML = '<a href="https://tradingview.github.io/lightweight-charts/">Made By DrJuneMoone</a>';
       row_{{ series.series_name }}.style.color = 'orange';
       legend.appendChild(row_{{ series.series_name }});
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
       chart.subscribeClick(function (param) {
         console.log(`An user clicks at (${param.point.x}, ${param.point.y}) point, the time is ${param.time}`);
       });
       chart.unsubscribeClick(function (param) {
         // Don’t get notified when a mouse clicks on a chart
       });
       chart.subscribeCrosshairMove(param => {
        if (!param.point) {
          return;
        }
        if (param.time) {
           const data = param.seriesData.get(chart_series_{{ series.series_name }});
           if ('{{ series.series_name }}' === 'ohlc') {
             const open = data.open !== undefined ? data.open : data.value;
             const high = data.high !== undefined ? data.high : data.value;
             const low = data.low !== undefined ? data.low : data.value;
             const close = data.close !== undefined ? data.close : data.value;
             row_{{ series.series_name }}.innerHTML = `<strong>open: ${open.toFixed(2)} | high: ${high.toFixed(2)} | low: ${low.toFixed(2)} | close: ${close.toFixed(2)}</strong>`;
           } else {
             const price = data.value !== undefined ? data.value : data.close;
             row_{{ series.series_name }}.innerHTML = `<strong>{{ series.series_name }}: ${price.toFixed(2)}`;
           }         
         } else {
             console.log(`A user moved the crosshair to (${param.point.x}, ${param.point.y}) point, the time is ${param.time}`);
         }
       });
       chart.timeScale().fitContent();
     })();
     {% endfor %}
      window.addEventListener("resize", () => {
        this.chart.resize(window.innerWidth, window.innerHeight);
      });
     })();
      const data_url = "{{ data_url }}";
      this.data_url = data_url;
      function updateData() {
          try {
              return axios({
                      method: 'GET',
                      url: document.location.href.replace('chart','data'),
                      crossOrigin: '*',
                  })
                  .then(response => {
                      {% for series in chart.series %}
                      this.chart_series_{{ series.series_name }}.update(response.data.{{ series.series_name }}[0])
                      {% endfor %}
                  })
          } catch (error) {
              throw {
                  code: error.code,
                  message: error.message,
                  responseStatus: error.response ? error.status : null,
                  url: url,
              };
          }
      }
      function setDataUpdateInterval()
      {
          var currentDateSeconds = new Date().getSeconds();
          if (currentDateSeconds == 0) {
              setInterval(updateData, 60000);
          }
          else {
              setTimeout(function () {
                  setDataUpdateInterval();
              }, (60 - currentDateSeconds) * 1000);
          }
          updateData();
      }
      setDataUpdateInterval();
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
     this.chart = chart;
     const container = document.getElementById("{{ output_div }}");
     const legend = document.createElement('div');
     legend.style = `position: absolute; left: 10px; top: 10px; z-index: 1; font-size: 10px; font-family: sans-serif; line-height: 14px; font-weight: 200;`;
     container.appendChild(legend);
     {% for series in chart.series %}
     (() => {
       const row_{{ series.series_name }} = document.createElement('div');
       row_{{ series.series_name }}.innerHTML = '<a href="https://tradingview.github.io/lightweight-charts/">Made By DrJuneMoone</a>';
       row_{{ series.series_name }}.style.color = 'orange';
       legend.appendChild(row_{{ series.series_name }});
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
       chart.subscribeClick(function (param) {
         console.log(`An user clicks at (${param.point.x}, ${param.point.y}) point, the time is ${param.time}`);
       });
       chart.unsubscribeClick(function (param) {
         // Don’t get notified when a mouse clicks on a chart
       });
       chart.subscribeCrosshairMove(param => {
        if (!param.point) {
          return;
        }
        if (param.time) {
           const data = param.seriesData.get(chart_series_{{ series.series_name }});
           if ('{{ series.series_name }}' === 'ohlc') {
             const open = data.open !== undefined ? data.open : data.value;
             const high = data.high !== undefined ? data.high : data.value;
             const low = data.low !== undefined ? data.low : data.value;
             const close = data.close !== undefined ? data.close : data.value;
             row_{{ series.series_name }}.innerHTML = `<strong>open: ${open.toFixed(2)} | high: ${high.toFixed(2)} | low: ${low.toFixed(2)} | close: ${close.toFixed(2)}</strong>`;
           } else {
             const price = data.value !== undefined ? data.value : data.close;
             row_{{ series.series_name }}.innerHTML = `<strong>{{ series.series_name }}: ${price.toFixed(2)}`;
           }         
         } else {
             console.log(`A user moved the crosshair to (${param.point.x}, ${param.point.y}) point, the time is ${param.time}`);
         }
       });
       chart.timeScale().fitContent();
     })();
     {% endfor %}
     })();
       const data_url = "{{ data_url }}";
       function updateData() {
          try {
              return axios({
                      method: 'GET',
                      url: data_url,
                      crossOrigin: '*',
                  })
                  .then(response => {
                      {% for series in chart.series %}
                      this.chart_series_{{ series.series_name }}.update(response.data.{{ series.series_name }}[0])
                      {% endfor %}
                  })
          } catch (error) {
              throw {
                  code: error.code,
                  message: error.message,
                  responseStatus: error.response ? error.status : null,
                  url: url,
              };
          }
      }
      function setDataUpdateInterval()
      {
          var currentDateSeconds = new Date().getSeconds();
          if (currentDateSeconds == 0) {
              setInterval(updateData, 60000);
          }
          else {
              setTimeout(function () {
                  setDataUpdateInterval();
              }, (60 - currentDateSeconds) * 1000);
          }
          updateData();
      }
      setDataUpdateInterval();
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


def _render(notebook_mode: bool,
            chart: _ChartSpec,
            data_url: str = "http://127.0.0.1:5000/data",
            base_url: str = "https://unpkg.com/lightweight-charts/dist/",
            output_div: str = "vis") -> str:
  """Render a model as html for viewing."""
  return (
      _TEMPLATES.render(chart=chart, data_url=data_url, base_url=base_url, output_div=output_div)
      if notebook_mode
      else _TEMPLATE.render(chart=chart, data_url=data_url, base_url=base_url, output_div=output_div)
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
               notebook_mode: bool = True,
               data_url: str = "http://127.0.0.1:5000/data",
               base_url: str = "https://unpkg.com/lightweight-charts/dist/",
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
    self.notebook_mode = notebook_mode
    self.data_url = data_url
    self.base_url = base_url
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
    return _render(
        notebook_mode=self.notebook_mode,
        chart=self._spec(),
        data_url=self.data_url,
        base_url=self.base_url,
        output_div=f'vis-{uuid.uuid4().hex}'
    )
