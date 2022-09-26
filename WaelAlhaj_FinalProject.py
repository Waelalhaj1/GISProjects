def hawkid():
    return(["Wael Alhaj", "Alhaj"])
hawkid()

print ("-------------------------------------------------------------------------------")
print ("1- Files preprations")
print ("A)Convert the CSV file of the Volcano coordinates to point shapefile and store it in the result geodatabase")

def volcanoShapeFile(inTable, xField, yField, workspace = "data/", geodatabase = "result.gdb"):
        
        '''
This function Convert the CSV file of the Volcano coordinates to point shapefile
and store it in the result geodatabase
        '''
        import arcpy
        import sys
        import os
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        try :
         #Create out put geodatabase
         arcpy.CreateFileGDB_management(arcpy.env.workspace, geodatabase)
        # featureTables = arcpy.ListTables()
         featureTables = arcpy.ListTables(inTable)
         for i in featureTables: 
        # check if the table class exists
          if inTable not in featureTables:
            print ("Table class " + inTable + " does not exist in " + workspace)
            sys.exit(-1)
          else:
            print ("Table class " + inTable + " exists in " + workspace)
            
        # check if the xField is in the list of field names

         fc_fieldnames = [f.name for f in arcpy.ListFields(inTable)]
         if xField not in fc_fieldnames:
            print ("The attribute is not in field names!")
            sys.exit(-1)
            
        # check if the yField is in the list of field names
         fc_fieldnames = [f.name for f in arcpy.ListFields(inTable)]
         if yField not in fc_fieldnames:
            print ("The attribute is not in field names!")
            sys.exit(-1)
            
    # create a point feature class for the stations 
         out_Layer = "volcano_lyr"
         saved_Layer = arcpy.env.workspace
    # select WGS 84 projection.
         spRef = arcpy.SpatialReference(4326)
        
         arcpy.MakeXYEventLayer_management(inTable, xField, yField, out_Layer, spRef)
         volcano= arcpy.CopyFeatures_management("volcano_lyr", "volcanoLocation")
        #export the volano shapefile to the out put geodatabase

         # check whether the spatial reference is a projected coordinate system - 0 means geographic coordinated system
         spRef = arcpy.SpatialReference(102661)
         projected_volc = "volcano_proj.shp"
         describe_fc2 = arcpy.Describe(volcano)
         if describe_fc2.spatialReference.PCSCode == 0:
            print ("WARNING:this shapefile has a geographic coordinate system.")
            
            #select NAD 1983 StatePlane Hawaii 1 FIPS 5101 (US Feet) projection.
           
            arcpy.Project_management(volcano, workspace+"/"+projected_volc, spRef)

         #save the out put point shapefile in the result geodatabase 
         arcpy.CopyFeatures_management( projected_volc, geodatabase +"/"+ "volcano")
         
        except arcpy.ExecuteError:
          print(arcpy.GetMessages())

volcanoShapeFile("volceno.csv", "x", "y")
print ("the volcano coordinate feature class saved in the result geodatabase.")
print ("-------------------------------------------------------------------------------")

print ("B) select by attribute the Hawaii county polygon shapefile and save it in result geodatabase.")


def hawaiiSapefile(fcpolygon, attribute, workspace = "data/", geodatabase = "result.gdb"):
        
        
        '''
  This function select by attribute the Hawaii county polygon shapefile
  and save it in result geodatabase.
        '''

        import arcpy
        import sys
        import os
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        try :
                
              featureClassList = arcpy.ListFeatureClasses(fcpolygon)

         # check if the feature class exists
              if fcpolygon not in featureClassList:
                 print ("Feature class " + fcpolygon + " does not exist in " + workspace)
                 sys.exit(-1)
              else:
                  print ("Feature class " + fcpolygon + " exists in " + workspace)
        
         # check if the input shape type is polygon
              describe_fc = arcpy.Describe(fcpolygon)
              if describe_fc.ShapeType != "Polygon":
                   print ("The input shape type is not a polygon!")
                   sys.exit(-1)
        # check if the attribute is in the list of field names
              fc_fieldnames = [f.name for f in arcpy.ListFields(fcpolygon)]
              if attribute not in fc_fieldnames:
                  print ("The attribute is not in field names!")
                  sys.exit(-1)
         
        # check whether the spatial reference is a projected coordinate system - 0 means geographic coordinated system
        #select NAD 1983 StatePlane Hawaii 1 FIPS 5101 (US Feet) projection.
              spRef = arcpy.SpatialReference(102661)
              projected = "Hawaii_proj.shp"
              if describe_fc.spatialReference.PCSCode == 0:
                  print ("WARNING: " + fcpolygon + " has a geographic coordinate system.")
             
           
              arcpy.Project_management(fcpolygon, workspace+"/"+projected, spRef)
        #select by attribute.  
              fcPolygonLayer = "polygon_lyr"      
              arcpy.MakeFeatureLayer_management(projected,fcPolygonLayer)
              expression = '"' + attribute + '" = ' + "'" + "Hawaii" + "'"
              arcpy.SelectLayerByAttribute_management(fcPolygonLayer, "NEW_SELECTION", expression)
              c= arcpy.CopyFeatures_management(fcPolygonLayer, "hawaiicounty")
         #Save the out put in the result geodatabase
              arcpy.CopyFeatures_management( c, geodatabase +"/"+ "HawaiiCounty")
         
        except arcpy.ExecuteError:
            print (arcpy.GetMessages())
hawaiiSapefile("costline.shp","isle")
print ("Hawaii county feature class saved in the result geodatabase.")
print ("-------------------------------------------------------------------------------")

print ("C) select by location the Hawaii county population point shapefile and save it in result geodatabase.")
print ("WARNING: this step may take time because the population block group shapefile is large.")

def hawaiipopulation (blockgroup,fcpolygon, attribute, workspace = "data/", geodatabase = "result.gdb"):
        
        '''
    This function selects by location the Hawaii county population point shapefile
    and save it in result geodatabase.
        '''
    
        import arcpy
        import sys
        import os
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        try:
           featureClassList = arcpy.ListFeatureClasses(blockgroup)

         # check if the feature class exists
           if blockgroup not in featureClassList:
              print ("Feature class " + blockgroup + " does not exist in " + arcpy.env.workspace)
              sys.exit(-1)
           else:
              print ("Feature class " + blockgroup + " exists in " + arcpy.env.workspace)
        # check if the attribute is in the list of field names
           fc_fieldnames = [f.name for f in arcpy.ListFields(blockgroup)]
           if attribute not in fc_fieldnames:
              print ("The attribute is not in field names!")
              sys.exit(-1)
            
        # check whether the spatial reference is a projected coordinate system - 0 means geographic coordinated system.
        #select NAD 1983 StatePlane Hawaii 1 FIPS 5101 (US Feet) projection.
           spRef = arcpy.SpatialReference(102661)
           projected_pop = "blockPop_proj.shp"
           describe_fc1 = arcpy.Describe(blockgroup)
           if describe_fc1.spatialReference.PCSCode == 0:
              print ("WARNING: " + blockgroup + " has a geographic coordinate system.")
            
              arcpy.Project_management(blockgroup, workspace+"/"+projected_pop, spRef)

         #select by location the population in the Hawaii county boundry.
           fcpointLayer = "point_lyr"
           arcpy.MakeFeatureLayer_management(projected_pop,fcpointLayer)
           arcpy.SelectLayerByLocation_management(fcpointLayer,"INTERSECT", fcpolygon)
           M= arcpy.CopyFeatures_management(fcpointLayer, "hawaiipop")
          #save the Hawaii county population feature class in the result geodatabase.
           arcpy.CopyFeatures_management( M, geodatabase +"/"+ "Hawaiipop")
        
        except arcpy.ExecuteError:
          print(arcpy.GetMessages())
hawaiipopulation ("blockpopulation.shp","hawaiicounty.shp","POP2010")
print ("The Hawaii county population saved in the result geodatabase.")
print ("-------------------------------------------------------------------------------")

print ("D) Moscic the rasters that coverd Hawaii county and save it in result geodatabase.")

def RasterPrep (tif1,tif2,tif3,tif4,tif5, tif6,fcplygon, workspace ="data/", geodatabase= "result.gdb"):

        '''
This function Moscics the rasters that coverd Hawaii county and save it in result geodatabase.
        '''
        import arcpy
        import sys
        import os
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        
        arcpy.CheckOutExtension("Spatial") 
        try:
            rasters = arcpy.ListRasters()
            #for i in rasters: 
        # check if the Raster exists
            if arcpy.Exists(tif1):
                print ("The raster " + tif1 + " exists in " + workspace)
                  
            else:
                print ("the raster  " + tif1 + " does not exist in " + workspace)
                sys.exit(-1)
 
        # check if The raster exists
            if arcpy.Exists(tif2):
                print ("The raster " + tif2 + " exists in " + workspace)
                  
            else:
                print ("The raster " + tif2 + " does not exist in " + workspace)
                sys.exit(-1)

           
        # check if The raster exists
            if arcpy.Exists(tif3):
                print ("The raster " + tif3 + " exists in " + workspace)
                  
            else:
                print ("The raster" + tif3 + " does not exist in " + workspace)
                sys.exit(-1)

        # check if The raster exists
            if arcpy.Exists(tif4):
                print ("The raster " + tif4 + " exists in " + workspace)
                  
            else:
                print ("The raster " + tif4 + " does not exist in " + workspace)
                sys.exit(-1)


        # check if The raster exists
            if arcpy.Exists(tif5):
                print ("The raster " + tif5 + " exists in " + workspace)
                  
            else:
                print ("The raster " + tif5 + " does not exist in " + workspace)
                sys.exit(-1)
  
        # check if the table class exists
            if arcpy.Exists(tif6):
                print ("The raster " + tif6 + " exists in " + workspace)
                  
            else:
                print ("The raster " + tif6 + " does not exist in " + workspace)
                sys.exit(-1)


            #Mosaic several TIFF images to a new TIFF image
            # set local variables
            ras_list = ";".join(rasters)  
            mosic_tif = "MosaicNew"
            out ="landnew.tif"
            masked_raster = "rasters"
            intr = "raster"
            spRef = arcpy.SpatialReference(102661)
            arcpy.env.mask = fcplygon
            output= arcpy.MosaicToNewRaster_management(ras_list, workspace, \
                                   out,spRef,\
                                   "8_BIT_UNSIGNED","0.0002","1")

            # Extract by Mask 
            outExtractByMask = arcpy.sa.ExtractByMask(out, fcplygon)
            outExtractByMask.save(workspace+"/"+ geodatabase+"/"+masked_raster)
            #convert the raster from float to intger type and save it in result geodatabase
            outInt =  arcpy.sa.Int(workspace+"/"+ geodatabase+"/"+masked_raster)
            outInt.save(workspace+"/"+ geodatabase+"/"+intr)
            #delete the float raster
            #arcpy.Delete_management(geodatabase+"/"+masked_raster)
            
        except arcpy.ExecuteError:
            print (arcpy.GetMessages())

RasterPrep ("tif1.tif","tif2.tif","tif3.tif","tif4.tif","tif5.tif", "tif6.tif","hawaiicounty.shp")
print ("Hawaii dem raster saved in result geodatabase")
print ("-------------------------------------------------------------------------------")

print ("2-  Fill the sink, calculate the flowdirection and flow accumulation and save the rasters in result geodatabase.")
print ("User should input the full full directory path of the result geodatabase.")
print ("For example: C:/Users/goodm/Desktop/final/data/result.gdb")
def fill(raster):

        '''

This function Fill the sink, calculate the flowdirection and flow accumulation
and save the rasters in result geodatabase.
        '''
        workspace = raw_input("Enter the full directory path of the result geodatabase: ")
        import arcpy
        import sys
        import os
        arcpy.env.workspace = str(workspace)
        arcpy.env.overwriteOutput = True
        arcpy.CheckOutExtension("Spatial")
                
        try:
        # set local variables
            FillRater = workspace+"\\"+"Fill"
            flowDir =   workspace+"\\"+"FlowDir"
            flow_acc =  workspace+"\\"+"FlowAcc"
           # check raster exist
            if arcpy.Exists(raster):
                print ("Raster class " + raster + " exists in " + workspace)
                  
            else:
                print ("Raster class " + raster + " does not exist in " + workspace)
                sys.exit(-1)
        
           # Execute Fill of sink
            outFill=arcpy.sa.Fill(raster)
            # Save the output
            outFill.save(FillRater)
            # Execute FlowDirection
            outFlowDirection = arcpy.sa.FlowDirection(outFill, "NORMAL")
            # Save the output
            outFlowDirection.save(flowDir)
            #Calculate flow accumulation
            flow_accum = arcpy.sa.FlowAccumulation(outFlowDirection)
            # Save the output
            flow_accum.save(flow_acc)

        
           
        except arcpy.ExecuteError:
            print (arcpy.GetMessages())
        
fill("raster")
print ("Fill , Flow direction and flow accumulation saved in the result geodatabase.")
print ("-------------------------------------------------------------------------------")

print ("3- calculate the Hawaii county streams and converted to line feature and save it in result geodatabase.")

def stream (flowDir,flow_acc, fcpolygon, workspace = "data\\result.gdb"):
        '''
This function calculates the Hawaii county streams and converted to line feature and save it in result geodatabase.
        '''
        import arcpy
        import sys
        import os
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        arcpy.CheckOutExtension("Spatial")
        try:
             featureClassList = arcpy.ListFeatureClasses(fcpolygon)

         # check if the feature class exists
             if fcpolygon not in featureClassList:
                  print ("Feature class " + fcpolygon + " does not exist in " + workspace) 
                  sys.exit(-1)
             else:
                  print ("Feature class " + fcpolygon + " exists in " + workspace)
        
            # check if the input shape type is polygon
             describe_fc = arcpy.Describe(fcpolygon)
             if describe_fc.ShapeType != "Polygon":
                  print ("The input shape type is not a polygon!")
                  sys.exit(-1)

             if arcpy.Exists(flowDir):
                print ("Raster class " + flowDir + " exists in " + workspace)
                  
             else:
                print ("Raster class " + flowDir + " does not exist in " + workspace)

             if arcpy.Exists(flow_acc):
                print ("Raster class " + flow_acc + " exists in " + workspace)
                  
             else:
                print ("Raster class " + flow_acc + " does not exist in " + workspace)
                sys.exit(-1)
            # set local variables 
             waterMask = "waterMask"
             HawaiiWater = "HawaiiWater"
             streamFeature = "HawaiiStreams"
             intFloDir = "intFloDir"
             # Extract by mask
             outExtractByMask = arcpy.sa.ExtractByMask(flow_acc, fcpolygon)
             outExtractByMask.save(workspace+"/"+waterMask)
             # raster calcultor Any flows with greater value than 2000 was considered as stream.
             outCon2 = arcpy.sa.Con( arcpy.sa.Raster(waterMask) >= 2000, 1)
             outCon2.save(workspace+"\\"+ HawaiiWater)
             # convert the float raster to integer.
             outInt =  arcpy.sa.Int(workspace+"/"+flowDir)
             outInt.save(workspace+"/"+intFloDir)
             # stream to feature 
             arcpy.sa.StreamToFeature(HawaiiWater, intFloDir, workspace+"\\"+streamFeature)

        except arcpy.ExecuteError:
            print (arcpy.GetMessages())            

stream ("FlowDir","FlowAcc","HawaiiCounty")

print ("stream to feature feature class is saved in the result geodatabase.")
print ("-------------------------------------------------------------------------------")

print ("4-  create 30 km and 45 km feature classes around the volcano and save them in result geodatabase.")

def buffer (fcPoint,distance1, distance2, distanceUnit, geodatabase= "data/result.gdb"):
    import arcpy
    import sys
    arcpy.env.workspace = geodatabase
    arcpy.env.overwriteOutput = True

    try:
        featureClassList = arcpy.ListFeatureClasses(fcPoint)

        # check if the feature class exists
        if fcPoint in featureClassList:
            print ("Feature classes " + fcPoint + " exists in " + geodatabase)
        else:
            print ("Missing feature class " + fcPoint + " in " + geodatabase)
            sys.exit(-1)

        # create describe objects for checking shape type
        desc_fcPoint = arcpy.Describe(fcPoint)
        if desc_fcPoint.shapeType != "Point":
            print ("ERROR: Feature class " + fcPoint + " is NOT a Point type!") 
            sys.exit(-1)
        
        # valid distance unit options for buffer
        distOptions = [["meters", "Meters", "meter", "Meter", "m"], 
                       ["kilometers", "Kilometers", "kilometer", "kilometers", "km"], 
                       ["miles", "Miles","mile", "Mile", "mi"], 
                       ["yards", "Yards", "yard", "Yard", "y"],
                       ["nautical miles", "Nautical Miles", "nautical mile", "Nautical Mile", "nm"],
                       ["feet", "Feet", "foot", "ft"],
                       ["decimal degrees", "Decimal Degrees", "decimal degree", "Decimal Degree", "dd"]]
        # check if the input distance unit is valid
        if distanceUnit in distOptions[0]: 
            distanceUnit = "Meters"
        elif distanceUnit in distOptions[1]:
            distanceUnit = "Kilometers"
        elif distanceUnit in distOptions[2]:
            distanceUnit = "Miles"
        elif distanceUnit in distOptions[3]:
            distanceUnit = "Yards"
        elif distanceUnit in distOptions[4]:
            distanceUnit = "NauticalMiles"
        elif distanceUnit in distOptions[5]:
            distanceUnit = "Feet"
        elif distanceUnit in distOptions[6]:
            distanceUnit = "DecimalDegrees"
        else:
            print ("ERROR: Invalid distance unit: " + distanceUnit)
            sys.exit(-1)
        # buffer expression
        bufferExpression = str(distance1) + " " + str(distanceUnit)

        # create a 30 km buffer feature class
        fcBuffer1 = geodatabase+"/"+fcPoint + "_buf30"
        arcpy.Buffer_analysis(fcPoint, fcBuffer1, bufferExpression, "", "ROUND")
        print ("Buffers from " + fcPoint + " were created and saved in the feature class " + fcBuffer1)


        bufferExpression = str(distance2) + " " + str(distanceUnit)
        # create a 45 km buffer feature class
        fcBuffer2 = geodatabase+"/"+fcPoint + "_buf45"
        arcpy.Buffer_analysis(fcPoint, fcBuffer2, bufferExpression, "", "ROUND")
        print ("Buffers from " + fcPoint + " were created and saved in the feature class " + fcBuffer2)

                 
    except arcpy.ExecuteError:
            print (arcpy.GetMessages())
buffer ("volcano",100000, 147638, "feet")

print ("30 km and 45 km buffers are created and saved in the result geodatabase.")
print ("-------------------------------------------------------------------------------")

print ("5- Select by location the streams and population inside the 30 km and 45 km ashes area")
print ("And calculate the total length of streams and population inside each buffer zone.")
def selection(fcBuffer1, fcBuffer2, streamFeature ,Hawaiipop, geodatabase= "data/result.gdb"):

        '''
This function Select by location the streams and population inside the 30 km and 45 km ashes area
And calculate the total length of streams and population inside each buffer zone.
         '''

        import arcpy
        import sys
        arcpy.env.workspace = geodatabase
        arcpy.env.overwriteOutput = True
        global str
        try:
             featureClassList = arcpy.ListFeatureClasses(fcBuffer1)

         # check if the feature class exists
             if fcBuffer1 not in featureClassList:
                  print ("Feature class " + fcBuffer1 + " does not exist in " + arcpy.env.workspace) 
                  sys.exit(-1)
             else:
                  print ("Feature class " + fcBuffer1 + " exists in " + arcpy.env.workspace)
        
            # check if the input shape type is polygon
             describe_fc = arcpy.Describe(fcBuffer1)
             if describe_fc.ShapeType != "Polygon":
                  print ("The input shape type is not a polygon!")
                  sys.exit(-1)

             featureClassList = arcpy.ListFeatureClasses(fcBuffer2)

         # check if the feature class exists
             if fcBuffer2 not in featureClassList:
                  print ("Feature class " + fcBuffer2 + " does not exist in " + arcpy.env.workspace) 
                  sys.exit(-1)
             else:
                  print ("Feature class " + fcBuffer2 + " exists in " + arcpy.env.workspace)
        
            # check if the input shape type is polygon
             describe_fc1 = arcpy.Describe(fcBuffer2)
             if describe_fc1.ShapeType != "Polygon":
                  print ("The input shape type is not a polygon!")
                  sys.exit(-1)

             featureClassList = arcpy.ListFeatureClasses(streamFeature)

         # check if the feature class exists
             if streamFeature not in featureClassList:
                  print ("Feature class " + streamFeature + " does not exist in " + arcpy.env.workspace) 
                  sys.exit(-1)
             else:
                  print ("Feature class " + streamFeature + " exists in " + arcpy.env.workspace)
        
            # check if the input shape type is polygon
             describe_fc2 = arcpy.Describe(streamFeature)
             if describe_fc2.ShapeType != "Polyline":
                  print ("The input shape type is not a polyline!")
                  sys.exit(-1)

             featureClassList = arcpy.ListFeatureClasses(Hawaiipop)

         # check if the feature class exists
             if Hawaiipop not in featureClassList:
                  print ("Feature class " + Hawaiipop + " does not exist in " + arcpy.env.workspace) 
                  sys.exit(-1)
             else:
                  print ("Feature class " + Hawaiipop + " exists in " + arcpy.env.workspace)
        
            # check if the input shape type is polygon
             describe_fc3 = arcpy.Describe(Hawaiipop)
             if describe_fc3.ShapeType != "Point":
                  print ("The input shape type is not a point!")
                  sys.exit(-1)
                  
            # set the local variables 
             lineLayer30 = "line30_lyr"
             stream30 = "stream30"
             lineLayer45 = "line45_lyr"
             stream45 = "stream45"
             pointLy30 = "point30_lyr"
             pop30 = "pop30"
             pointLy45 = "point45_lyr"
             pop45 = "pop45"

             #create 30 km streams feature class 
             arcpy.MakeFeatureLayer_management(streamFeature,lineLayer30)
             arcpy.SelectLayerByLocation_management(lineLayer30,"INTERSECT", fcBuffer1)
             arcpy.CopyFeatures_management(lineLayer30, stream30)
             #create 45 km streams feature class 
             arcpy.MakeFeatureLayer_management(streamFeature,lineLayer45)
             arcpy.SelectLayerByLocation_management(lineLayer45,"INTERSECT", fcBuffer2)
             arcpy.CopyFeatures_management(lineLayer45, stream45)
             #create 30 km population feature class 
             arcpy.MakeFeatureLayer_management(Hawaiipop,pointLy30)
             arcpy.SelectLayerByLocation_management(pointLy30,"INTERSECT", fcBuffer1)
             arcpy.CopyFeatures_management(pointLy30, pop30)
             #create 45 km population feature class 
             arcpy.MakeFeatureLayer_management(Hawaiipop,pointLy45)
             arcpy.SelectLayerByLocation_management(pointLy45,"INTERSECT", fcBuffer2)
             arcpy.CopyFeatures_management(pointLy45, pop45)
             print ("-------------------------------------------------------------------------------")
             print ("---------------------------------Results---------------------------------------")
             print ("1- Streams :")
# calculate the total length of streams in Hawaii county 
             
             convert = 0.000305   # convert factor from ft to km 
             totalLength = 0
             curs = arcpy.da.SearchCursor(streamFeature, ["Shape_Length"]) 
             for row in curs:
                totalLength += row[0]
                del row
             del curs
             #convert from ft to km
             totalLength = round ((totalLength * convert),2)
             print ("A) Total length of streams " + streamFeature + " is "+ str (totalLength) + " Km.")
             print ("-------------------------------------------------------------------------------")        
             
# calculate the total length of streams in range 30 km from volcano in Hawaii county 
             totalLength30 = 0
             curs = arcpy.da.SearchCursor(stream30, ["Shape_Length"]) 
             for row in curs:
                totalLength30 += row[0]
                del row
             del curs
             #convert from ft to km
             totalLength30 = round ((totalLength30 * convert),2)
             #calculate the precentage of the 30 km streams length 
             percentage = round((totalLength30/totalLength)*100.0,2)
             print ("B) Total length of streams " + stream30 + " is "+ str(totalLength30) + " Km.")
             print ("which is = "+ str (percentage) +" % of total Hawaii streams leangth")
             print ("-------------------------------------------------------------------------------")

# calculate the total length of streams in range 45 km from volcano in Hawaii county 
             totalLength45 = 0
             curs = arcpy.da.SearchCursor(stream45, ["Shape_Length"]) 
             for row in curs:
                totalLength45 += row[0]
                del row
             del curs
             #convert from ft to km
             totalLength45 = round ((totalLength45 * convert),2)
             #calculate the precentage of the 30 km streams length 
             percentage = round((totalLength45/totalLength)*100.0,2)
             print ("C) Total length of streams " + stream45 + " is "+ str (totalLength45) + " Km.")
             print ("which is = "+ str (percentage) +" % of total Hawaii streams leangth")
             print ("-------------------------------------------------------------------------------")
             print ("-------------------------------------------------------------------------------")

             print ("2- Population :")
# calculate the total 2010 population in Hawaii county 
             convert2 = 1.0
             totalPop = 0
             curs = arcpy.da.SearchCursor(Hawaiipop, ["POP2010"]) 
             for row in curs:
                totalPop += row[0]
                del row
             del curs
             
             print ("A) The Total Hawaii population is "+ str (totalPop))
        
             print ("-------------------------------------------------------------------------------")             
# calculate the total 2010 population in range of 30 km from volcano in Hawaii county
             totalPop30 = 0
             curs = arcpy.da.SearchCursor(pop30, ["POP2010"]) 
             for row in curs:
                totalPop30 += row[0]
                del row
             del curs
             totalPop30 =round ((totalPop30 * convert2),2)
             #calculate the precentage of the 30 km 2010 population
             percentage1 = round((totalPop30/totalPop)*100.0,2)
             print ("B) The total population in 30 km ashes area is "+ str(totalPop30))
             print ("which is = "+ str (percentage1) +" % of total Hawaii population")
             
             print ("-------------------------------------------------------------------------------")             
# calculate the total 2010 population in range of 45 km from volcano in Hawaii county
             totalPop45 = 0
             curs = arcpy.da.SearchCursor(pop45, ["POP2010"]) 
             for row in curs:
                totalPop45 += row[0]
                del row
             del curs
             totalPop45 =round ((totalPop45 * convert2),2)
             #calculate the precentage of the 30 km 2010 population
             percentage2 = round((totalPop45/totalPop)*100.0,2)
             print ("C) The total population in 45 km ashes area is "+ str(totalPop45))
             print ("which is = "+ str (percentage2) +" % of total Hawaii population")
            
             print ("-------------------------------------------------------------------------------")
             print ("-------------------------------------------------------------------------------")
        except arcpy.ExecuteError:
            print (arcpy.GetMessages())
            
selection("volcano_buf30", "volcano_buf45", "HawaiiStreams" ,"Hawaiipop")

print ("All the results are printed and the project is done!.")
print ("-------------------------------------------------------------------------------")
        

        


             
             

             

                
                
        

        



