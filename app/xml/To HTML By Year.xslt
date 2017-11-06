<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

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

<xsl:template match="publication">
    <li>
    <!--Print Authors-->
    <xsl:apply-templates select="authors"/>
    <!--Print Title, include URL if available-->
    <xsl:text>"</xsl:text>
    <xsl:choose>
        <xsl:when test="url!=''"><a><xsl:attribute name="href"><xsl:value-of select="url"/></xsl:attribute>
            <xsl:value-of select="title"/></a>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="title"/>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:text>," </xsl:text>
    <!-- Print book -->
    <xsl:if test="type='Dissertation'">PhD Dissertation, </xsl:if>
    <xsl:if test="school!=''"><xsl:value-of select="school"/>, </xsl:if>
    <xsl:if test="book!=''"><i><xsl:value-of select="book"/></i>, </xsl:if>
    <!-- Print remaining details -->
    <xsl:if test="volume!=''">vol. <xsl:value-of select="volume"/>, </xsl:if>
    <xsl:if test="number!=''">no. <xsl:value-of select="number"/>, </xsl:if>
    <xsl:if test="pages!=''">pp. <xsl:value-of select="pages"/>, </xsl:if>
    <xsl:if test="location!=''"><xsl:value-of select="location"/>, </xsl:if>
    <xsl:choose>
        <xsl:when test="year!=''"><xsl:value-of select="month"/><xsl:text> </xsl:text><xsl:value-of select="year"/>.</xsl:when>
        <xsl:otherwise>to appear.</xsl:otherwise>
    </xsl:choose>
    <!-- Print notes -->
    <xsl:if test="notes!=''"> (<xsl:value-of select="notes"/>)</xsl:if>
    </li>
</xsl:template>

<xsl:template match="authors">
    <xsl:choose>
        <xsl:when test="count(./author)=2">
            <xsl:for-each select="author">
                <xsl:choose>
                    <xsl:when test="/bibliography/@owner = .">
                        <span class="name"><xsl:value-of select="."/></span>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:choose>
                    <xsl:when test="position() = 1"> and </xsl:when>
                    <xsl:otherwise>, </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:for-each select="author">
                <xsl:choose>
                    <xsl:when test="/bibliography/@owner = .">
                        <span class="name"><xsl:value-of select="."/></span>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:choose>
                    <xsl:when test="position() = last()-1">, and </xsl:when>
                    <xsl:otherwise>, </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>
