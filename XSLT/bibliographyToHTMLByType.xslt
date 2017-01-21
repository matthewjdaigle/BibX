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
    <xsl:if test="count(publication[type = 'Journal'])&gt;0">
        <h2>Journal</h2>
        <ul>
            <xsl:apply-templates select="publication[type = 'Journal']"/>
        </ul>
    </xsl:if>
    <xsl:if test="count(publication[type = 'Conference'])&gt;0">
        <h2>Refereed Proceedings</h2>
        <ul>
            <xsl:apply-templates select="publication[type = 'Conference']"/>
        </ul>
    </xsl:if>
    <xsl:if test="count(publication[type = 'Unrefereed'])&gt;0">
        <h2>Unrefereed Proceedings</h2>
        <ul>
            <xsl:apply-templates select="publication[type = 'Unrefereed']"/>
        </ul>
    </xsl:if>
    <xsl:if test="count(publication[type = 'Dissertation'])&gt;0">
        <h2>Theses</h2>
        <ul>
            <xsl:apply-templates select="publication[type = 'Dissertation']"/>
        </ul>
    </xsl:if>
    <xsl:if test="count(publication[type = 'Technical Report'])&gt;0">
        <h2>Technical Reports</h2>
        <ul>
            <xsl:apply-templates select="publication[type = 'Technical Report']"/>
        </ul>
    </xsl:if>
</xsl:template>

<xsl:include href="publicationHTML.xslt"/>

</xsl:stylesheet>

