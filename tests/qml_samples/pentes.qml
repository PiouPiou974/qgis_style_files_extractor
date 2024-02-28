<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" styleCategories="LayerConfiguration|Symbology|Symbology3D|Labeling|Fields|Forms|Actions|MapTips|Diagrams|AttributeTable|Rendering|Legend" minScale="1e+08" hasScaleBasedVisibilityFlag="0" version="3.34.3-Prizren">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <mapTip enabled="1"></mapTip>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option value="" type="QString" name="name"/>
      <Option name="properties"/>
      <Option value="collection" type="QString" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling enabled="false" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour" maxOversampling="2"/>
    </provider>
    <rasterrenderer classificationMin="0" nodataColor="" classificationMax="100" alphaBand="-1" type="singlebandpseudocolor" band="1" opacity="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader clip="0" maximumValue="100" colorRampType="INTERPOLATED" classificationMode="1" labelPrecision="4" minimumValue="0">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option value="247,251,255,0" type="QString" name="color1"/>
              <Option value="141,90,153,255" type="QString" name="color2"/>
              <Option value="ccw" type="QString" name="direction"/>
              <Option value="0" type="QString" name="discrete"/>
              <Option value="gradient" type="QString" name="rampType"/>
              <Option value="rgb" type="QString" name="spec"/>
              <Option value="0.25;255,158,23,255;rgb;ccw:0.5;231,113,72,255;rgb;ccw:0.75;196,60,57,255;rgb;ccw" type="QString" name="stops"/>
            </Option>
          </colorramp>
          <item value="0" color="#f7fbff" alpha="0" label="0,0000"/>
          <item value="25" color="#ff9e17" alpha="255" label="25,0000"/>
          <item value="50" color="#e77148" alpha="255" label="50,0000"/>
          <item value="75" color="#c43c39" alpha="255" label="75,0000"/>
          <item value="100" color="#8d5a99" alpha="255" label="100,0000"/>
          <rampLegendSettings useContinuousLegend="1" orientation="2" maximumLabel="" direction="0" minimumLabel="" prefix="" suffix="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="invalid" name="decimal_separator"/>
                <Option value="6" type="int" name="decimals"/>
                <Option value="0" type="int" name="rounding_type"/>
                <Option value="false" type="bool" name="show_plus"/>
                <Option value="true" type="bool" name="show_thousand_separator"/>
                <Option value="false" type="bool" name="show_trailing_zeros"/>
                <Option type="invalid" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" brightness="0" contrast="0"/>
    <huesaturation saturation="0" colorizeStrength="100" colorizeOn="0" colorizeBlue="128" grayscaleMode="0" colorizeGreen="128" invertColors="0" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
