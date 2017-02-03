<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="html" indent="yes"/>

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
        <h2>
            <xsl:if test="year = ''">Forthcoming</xsl:if>
            <xsl:value-of select="year" />
        </h2>
        <ul>
        <xsl:for-each select="key('publicationsByYear', year)">
            <xsl:apply-templates select="."/>
        </xsl:for-each>
        </ul>
    </xsl:for-each>
</xsl:template>

<xsl:include href="publicationHTML.xslt"/>

</xsl:stylesheet>

