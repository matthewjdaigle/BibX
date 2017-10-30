<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

<xsl:template match="/">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="bibliography">
    <xsl:apply-templates select="publication"/>
</xsl:template>

<xsl:template match="publication">
    <!--Print opening tag and id-->
    <xsl:choose>
        <xsl:when test="type='Book'">@book{</xsl:when>
        <xsl:when test="type='Journal'">@article{</xsl:when>
        <xsl:when test="type='Conference'">@conference{</xsl:when>
        <xsl:when test="type='Unrefereed'">@conference{</xsl:when>
        <xsl:when test="type='Technical Report'">@techreport{</xsl:when>
        <xsl:when test="type='Dissertation'">@phdthesis{</xsl:when>
        <xsl:otherwise>@misc{</xsl:otherwise>
    </xsl:choose><xsl:value-of select="@id"/><xsl:text>,</xsl:text>
    <!--Print Authors, Title-->
    author = {<xsl:apply-templates select="authors"/>},
    title = {<xsl:value-of select="title"/>},
    <xsl:if test="school!=''">school = {<xsl:value-of select="school"/>},&#10;</xsl:if>
    <xsl:if test="book!=''">book = {<xsl:value-of select="book"/>},&#10;</xsl:if>
    <!-- Print remaining details -->
    <xsl:if test="volume!=''">    volume = {<xsl:value-of select="volume"/>},&#10;</xsl:if>
    <xsl:if test="number!=''">    number = {<xsl:value-of select="number"/>},&#10;</xsl:if>
    <xsl:if test="pages!=''">    pages = {<xsl:value-of select="pages"/>},&#10;</xsl:if>
    <xsl:if test="location!=''">    location = {<xsl:value-of select="location"/>},&#10;</xsl:if>
    <xsl:if test="month!=''">    month = {<xsl:value-of select="month"/>},&#10;</xsl:if>
    <xsl:if test="year!=''">    year = {<xsl:value-of select="year"/>},&#10;</xsl:if>
    <xsl:text>}&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
</xsl:template>

<xsl:template match="authors">
    <xsl:for-each select="author">
        <xsl:value-of select="."/>
        <xsl:if test="position() != last()"> and </xsl:if>
    </xsl:for-each>
</xsl:template>

</xsl:stylesheet>

