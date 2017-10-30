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
    <!--Print Authors, Title-->
    <xsl:apply-templates select="authors"/>"<xsl:value-of select="title"/><xsl:text>," </xsl:text> 
    <!-- Print book -->
    <xsl:if test="type='dissertation'">PhD Dissertation, </xsl:if>
    <xsl:if test="school!=''"><xsl:value-of select="school"/>, </xsl:if>
    <xsl:if test="book!=''"><xsl:value-of select="book"/>, </xsl:if>
    <!-- Print remaining details -->
    <xsl:if test="volume!=''">vol. <xsl:value-of select="volume"/>, </xsl:if>
    <xsl:if test="number!=''">no. <xsl:value-of select="number"/>, </xsl:if>
    <xsl:if test="pages!=''">pp. <xsl:value-of select="pages"/>, </xsl:if>
    <xsl:if test="location!=''"><xsl:value-of select="location"/>, </xsl:if>
    <xsl:choose>
        <xsl:when test="year!=''">
            <xsl:value-of select="month"/><xsl:text> </xsl:text><xsl:value-of select="year"/>.</xsl:when>
        <xsl:otherwise>to appear.</xsl:otherwise>
    </xsl:choose>
    <!-- Print notes -->
    <xsl:if test="notes!=''"> (<xsl:value-of select="notes"/>)</xsl:if>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
</xsl:template>

<xsl:template match="authors">
    <xsl:choose>
        <xsl:when test="count(./author)=2">
            <xsl:for-each select="author">
                <xsl:value-of select="."/>
                <xsl:choose>
                    <xsl:when test="position() = 1"> and </xsl:when>
                    <xsl:otherwise>, </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:for-each select="author">
                <xsl:value-of select="."/>
                <xsl:choose>
                    <xsl:when test="position() = last()-1">, and </xsl:when>
                    <xsl:otherwise>, </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>

