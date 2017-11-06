<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text" indent="yes"/>

<xsl:template match="/">
    <html>
        <body>
            <xsl:apply-templates/>
        </body>
    </html>
</xsl:template>

<xsl:key name="publicationsByYear" match="publication" use="year" />

<xsl:template match="bibliography">
    <xsl:for-each select="publication[count(. | key('publicationsByYear', year)[1]) = 1]">
        <xsl:sort select="position()" data-type="number" order="ascending"/>

        <xsl:choose>
            <xsl:when test="year =''">- year: Forthcoming</xsl:when>
            <xsl:otherwise>- year: <xsl:value-of select="year"/></xsl:otherwise>
        </xsl:choose>
  publications:
        <xsl:for-each select="key('publicationsByYear', year)">
          <xsl:apply-templates select="."/>
          <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
        <xsl:text>&#xa;</xsl:text>
    </xsl:for-each>
</xsl:template>

<xsl:template match="publication">
    - title: "<xsl:value-of select="title"/>"
      authors: <xsl:apply-templates select="authors"/>
      url: <xsl:value-of select="url"/>
      type: <xsl:value-of select="type"/>
      school: <xsl:value-of select="school"/>
      book: "<xsl:value-of select="book"/>"
      volume: <xsl:value-of select="volume"/>
      number: <xsl:value-of select="number"/>
      pages: <xsl:value-of select="pages"/>
      location: <xsl:value-of select="location"/>
<xsl:text>&#xa;</xsl:text>
      <xsl:choose>
      <xsl:when test="year!=''">      year: <xsl:value-of select="year"/></xsl:when>
      <xsl:otherwise>      year: to appear</xsl:otherwise>
      </xsl:choose>
      month: <xsl:value-of select="month"/>
      notes: <xsl:value-of select="notes"/>
</xsl:template>

<xsl:template match="authors">
    <xsl:choose>
        <xsl:when test="count(./author)=2">
            <xsl:for-each select="author">
                <xsl:value-of select="."/>
                <xsl:choose>
                    <xsl:when test="position() = 1"> and </xsl:when>
                    <xsl:otherwise></xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:for-each select="author">
                <xsl:value-of select="."/>
                <xsl:choose>
                    <xsl:when test="position() = last()"></xsl:when>
                    <xsl:when test="position() = last()-1">, and </xsl:when>
                    <xsl:otherwise>, </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
