import numpy as np
import cairo

def drawSankeySvg(self, layoutIndex, sankeyDict): 
    def createText(context, text, centerx, centery):
        context.save()
        (x, y, width, height, dx, dy) = context.text_extents(text)
        textPosx = centerx - width/2 - x 
        textPosy = centery - height/2 - y
        context.set_source_rgba(*hfCols['bgText'])
        context.rectangle(textPosx-2, textPosy-height-3, width+7, height+8)
        context.fill()
        context.set_source_rgba(*hfCols['text'])
        context.move_to(textPosx, textPosy)
        context.show_text(text)
        context.restore()
        context.new_path()

    self.currentLayoutIndex = layoutIndex
    layoutName = self.cache['layouts'][layoutIndex]['name']
    svgWidth, svgHeight = 500, 500
    bgWidth, bgHeight = 0.9 * svgWidth, 0.9 * svgHeight
    self.svg.setFixedSize(svgWidth, svgHeight)
    layerCols = [
        (1.0, 0.701, 0.729),   # Pastellrosa
        (1.0, 0.874, 0.729),   # Pastellorange
        (1.0, 1.0, 0.729),     # Pastellgelb
        (0.729, 1.0, 0.788),   # Pastellgrün
        (0.729, 1.0, 1.0),     # Pastelltürkis
        (0.729, 0.882, 1.0),   # Pastellblau
        (0.855, 0.729, 1.0),   # Pastelllila
        (1.0, 0.729, 0.945),   # Pastellmagenta
        (0.941, 0.941, 0.941), # Hellgrau / Weißpastell
        (1.0, 0.8, 0.898)      # Zartes Rosa
    ]
    hfCols = {
        'bgText': (1.0, 1.0, 1.0, 0.5),
        'text': (0.0, 0.0, 0.0, 1.0),
        'endBlock': (0.0, 0.0, 0.0, 1.0), # black
        'heatConduct': (1.0, 0.0, 0.0, 0.7), # red
        'coldside': (0.0, 0.5019607843137255, 0.0, 0.7), # green
        'peltier': (0.0, 0.0, 1.0, 0.7), # blue
        'hotside': (1.0, 0.0, 1.0, 0.7), # violet
        'joule': (1.0, 0.6470588235294118, 0.0, 0.7), # orange
        'in': (1.0, 1.0, 0.0, 0.7) # yellow
    }
    structure = self.cache['layouts'][self.currentLayoutIndex]['thermalStructure']
    structureHeight = sum((layer['thickness'] for layer in structure))
    structureArea = max((layer['area'] for layer in structure))
    layoutName = self.cache['layouts'][self.currentLayoutIndex]['name']
    with cairo.SVGSurface(f"assets/outputSankey_{layoutName}.svg", svgWidth, svgHeight) as surface:
        ### draw background
        ct = cairo.Context(surface)
        ct.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ct.set_font_size(12)
        bgStartx = (svgWidth-bgWidth)/2
        bgStarty = (svgHeight-bgHeight)/2
        cumuThickness = bgStarty
        for i, layer in enumerate(structure):
            r = layerCols[i%len(layerCols)][0]
            g = layerCols[i%len(layerCols)][1]
            b = layerCols[i%len(layerCols)][2]
            ct.set_source_rgba(r, g, b, 0.2)
            height = layer['thickness'] / structureHeight * bgHeight
            if layer['area'] == structureArea: # full rectangle
                ct.rectangle(bgStartx, cumuThickness, bgWidth, height)
            else: # stripes
                coverage = (layer['area'] / structureArea)**(1/2)
                # nStripes = 5
                nStripes = round(self.cache['layouts'][self.currentLayoutIndex]['numberOfElectricalRepetitions']**(1/2))
                coveredArea = coverage * bgWidth
                blankArea = (1-coverage) * bgWidth
                stripeWidth = coveredArea / (nStripes + 1)
                gapWidth = blankArea / nStripes 
                x = bgStartx + (gapWidth + stripeWidth) / 2
                for i in range(nStripes):
                    ct.rectangle(x, cumuThickness, stripeWidth, height)
                    x += (stripeWidth + gapWidth)
            cumuThickness += height
            ct.fill()
        
        ### draw heatfluxi
        # > 0 check
        if any([val<0 for val in sankeyDict.values()]):
            createText(ct, f"Error: negative Heatfluxes", svgWidth/2, svgHeight/2)
        elif len(sankeyDict) == 0:
            createText(ct, f"Choose ΔT", svgWidth/2, svgHeight/2)
        elif (sankeyDict['P_Hotside'] + sankeyDict['P_HeatConduct']) == 0:
            createText(ct, f"Error: no Heatfluxes", svgWidth/2, svgHeight/2)
        else:
            # variables
            margin = 20
            hfStartx = bgStartx + margin
            hfStarty = bgStarty + margin
            hfEndx = bgStartx + bgWidth - margin
            hfEndy = bgStarty + bgHeight - margin
            hfMidx = (hfEndx + hfStartx)/2
            hfMidy = (hfEndy + hfStarty)/2

            hfPixelRatio = (bgWidth - 8 * margin) / (sankeyDict['P_Hotside'] + sankeyDict['P_HeatConduct'])
            PHotSideWidth = sankeyDict['P_Hotside'] * hfPixelRatio
            PJouleWidth = sankeyDict['P_Joule'] * hfPixelRatio
            PColdsideWidth = sankeyDict['P_Coldside'] * hfPixelRatio
            PHeatConductWidth = sankeyDict['P_HeatConduct'] * hfPixelRatio
            PPeltierWidth = sankeyDict['P_Peltier'] * hfPixelRatio
            PInWidth = sankeyDict['P_In'] * hfPixelRatio
            PSeebeckWidth = sankeyDict['P_Seebeck'] * hfPixelRatio

            PHotSideAndHeatConductWidth = PHotSideWidth + PHeatConductWidth

            # Heatconduct line
            heatConductX = hfMidx+((PHotSideAndHeatConductWidth)/2)-PHeatConductWidth/2
            ct.set_source_rgba(*hfCols['heatConduct'])
            ct.set_line_width(PHeatConductWidth)
            ct.move_to(heatConductX, hfEndy-margin)
            ct.line_to(heatConductX, hfStarty+margin)
            ct.stroke()
            # Heatconduct start and end block
            ct.set_source_rgba(*hfCols['endBlock'])
            ct.move_to(heatConductX, hfEndy)
            ct.line_to(heatConductX, hfEndy-margin)
            ct.stroke()
            ct.move_to(heatConductX, hfStarty)
            ct.line_to(heatConductX, hfStarty+margin)
            ct.stroke()
            
            # In start arrow
            ct.set_source_rgba(*hfCols['in'])
            ct.move_to(0, svgHeight/2+PInWidth/2)
            ct.line_to(margin, svgHeight/2)
            ct.line_to(0, svgHeight/2-PInWidth/2)
            ct.line_to(hfStartx+margin, svgHeight/2-PInWidth/2)
            ct.line_to(hfStartx+margin, svgHeight/2+PInWidth/2)
            ct.close_path()
            ct.fill()

            # seebeck end block
            ct.set_line_width(PSeebeckWidth)
            ct.set_source_rgba(*hfCols['endBlock'])
            ct.move_to(hfStartx, svgHeight/2+PInWidth/2-PSeebeckWidth/2)
            ct.line_to(hfStartx+margin, svgHeight/2+PInWidth/2-PSeebeckWidth/2)
            ct.stroke()

            # # Joule start line
            # ct.set_source_rgba(*hfCols['joule'])
            # ct.set_line_width(PJouleWidth)
            # ct.move_to(0, svgHeight/2)
            # ct.line_to(hfStartx, svgHeight/2)
            # ct.stroke()

            # Joule-Hotside-arc
            ct.set_line_width(PJouleWidth/2)
            ct.set_source_rgba(*hfCols['joule'])
            ct.save()
            ct.translate(hfStartx+margin, hfStarty+margin) # pos of ellipse center
            scalex = (hfMidx - PHotSideAndHeatConductWidth/2 + PJouleWidth/4) - hfStartx - margin
            scaley = (hfMidy - PJouleWidth/4) - (hfStarty + margin) - PSeebeckWidth/2
            ct.scale(scalex, scaley)
            ct.arc(0.0, 0.0, 1.0, 0, 0.5*np.pi)
            ct.restore()
            ct.stroke()

            # Joule-Coldside endblock
            ct.set_source_rgba(*hfCols['endBlock'])
            ct.move_to(hfMidx-(PHotSideAndHeatConductWidth/2)+ 0.75 * PJouleWidth, hfEndy)
            ct.line_to(hfMidx-(PHotSideAndHeatConductWidth/2)+ 0.75 * PJouleWidth, hfEndy-margin)
            ct.stroke()

            # coldside start arrow
            ct.set_source_rgba(*hfCols['coldside'])
            ct.move_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth, svgHeight)
            ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth, hfEndy-margin)
            ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth, hfEndy-margin)
            ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth, svgHeight)
            ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth, svgHeight)
            ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth/2, svgHeight-margin)
            ct.close_path()
            ct.fill()

            # # Coldside Start Line
            # ct.set_source_rgba(*hfCols['coldside'])
            # ct.set_line_width(PColdsideWidth)
            # ct.move_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth/2, svgHeight)
            # ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth/2, hfEndy-margin)
            # ct.stroke()

            # HotSide End Arrow
            ct.set_source_rgba(*hfCols['hotside'])
            ct.move_to(hfMidx-PHeatConductWidth/2-PHotSideWidth/2, hfStarty+margin)
            ct.line_to(hfMidx-PHeatConductWidth/2-PHotSideWidth/2, margin)
            ct.line_to(hfMidx-PHeatConductWidth/2, 0)
            ct.line_to(hfMidx-PHeatConductWidth/2+PHotSideWidth/2, margin)
            ct.line_to(hfMidx-PHeatConductWidth/2+PHotSideWidth/2, hfStarty+margin)

            ct.close_path()
            ct.fill()

            # # HotSide End Line
            # ct.set_source_rgba(*hfCols['hotside'])
            # ct.set_line_width(PHotSideWidth)
            # ct.move_to(hfMidx - PHeatConductWidth/2, hfStarty+margin)
            # ct.line_to(hfMidx - PHeatConductWidth/2, 0)
            # ct.stroke()

            # Peltier Line
            ct.set_source_rgba(*hfCols['peltier'])
            ct.set_line_width(PPeltierWidth)
            ct.move_to(hfMidx + PHotSideAndHeatConductWidth/2 - PPeltierWidth/2, hfEndy-margin)
            ct.line_to(hfMidx + PHotSideAndHeatConductWidth/2 - PPeltierWidth/2, hfStarty+margin)
            ct.stroke()

            # Joule-Coldside-arc
            ct.set_line_width(PJouleWidth/2)
            ct.set_source_rgba(*hfCols['joule'])
            ct.save()
            ct.translate(hfStartx+margin, hfEndy-margin)
            scalex = (hfMidx - PHotSideAndHeatConductWidth/2 + PJouleWidth * 3/4) - hfStartx - margin
            scaley = (hfEndy - margin) - (hfMidy + PJouleWidth/4) + PSeebeckWidth/2
            ct.scale(scalex, scaley)
            ct.arc(0.0, 0.0, 1.0, 1.5*np.pi, 2*np.pi)
            ct.restore()
            ct.stroke()

            # labels
            decPlaces = 1 if sankeyDict['P_Coldside'] > 1 else 2
            createText(ct, f"P_ J ({sankeyDict['P_Joule']:.{decPlaces}f} W)", hfStartx+3*margin, hfMidy - PSeebeckWidth/2)
            createText(ct, f"P_S ({sankeyDict['P_Seebeck']:.{decPlaces}f} W)", hfStartx+3*margin, svgHeight/2+PInWidth/2-PSeebeckWidth/2)
            createText(ct, f"P_In ({sankeyDict['P_In']:.{decPlaces}f} W)", 3*margin, (hfMidy - PSeebeckWidth + svgHeight/2+PInWidth/2)/2 )
            createText(ct, f"P_HS ({sankeyDict['P_Hotside']:.{decPlaces}f} W)", hfMidx - PHeatConductWidth/2, 30)
            createText(ct, f"P_CS ({sankeyDict['P_Coldside']:.{decPlaces}f} W)", hfMidx+PHotSideAndHeatConductWidth/2-PHeatConductWidth-PColdsideWidth/2, svgHeight-30)
            createText(ct, f"P_Pe ({sankeyDict['P_Peltier']:.{decPlaces}f} W)", hfMidx + PHotSideAndHeatConductWidth/2 - PPeltierWidth/2, svgHeight/2-30)
            ct.set_line_width(5)
            ct.set_source_rgba(*hfCols['bgText'])
            ct.move_to(hfMidx+PHotSideAndHeatConductWidth/2-PPeltierWidth/2 - PPeltierWidth/2, svgHeight/2-19)
            ct.line_to(hfMidx+PHotSideAndHeatConductWidth/2-PPeltierWidth/2 + PPeltierWidth/2, svgHeight/2-19)
            ct.stroke()
            createText(ct, f"P_λ ({sankeyDict['P_HeatConduct']:.{decPlaces}f} W)", heatConductX+35, svgHeight/2+30)

    self.svg.load(f"assets/outputSankey_{layoutName}.svg")