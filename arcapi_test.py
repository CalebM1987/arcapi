"""
#-------------------------------------------------------------------------------
# Name:        arcapi_test
# Purpose:     Tests for arcapi module.
#
# Author:      Filip Kral
#
# Created:     01/02/2014
# Licence:     LGPL v3
#-------------------------------------------------------------------------------
# Most of the functions operate on potentially complex data, or require manual
# checking of results, and therefore testing is rather difficult.
#
# Everybody is encouraged to contribute to tests.
#-------------------------------------------------------------------------------
"""

import unittest
import os
import sys
import arcpy
import arcapi as ap

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        # access testing data
         try:
            self.testingfolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testing')
        except:
            self.testingfolder = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'testing')
        self.testing_gdb = os.path.join(self.testingfolder, 'testing.gdb')
        #self.t_table = os.path.join(self.testing_gdb, '\left_i_right')
        #self.t_fc =  os.path.join(self.testing_gdb, 'left_i_right')
        #self.t_cols = ('OBJECTID', 'Shape', 'CCARM2', 'POINT_X', u'POINT_Y', u'ROUND_X', 'ROUND_Y', 'name', 'propagatedName', 'fullName', 'GID', 'DOWNGID', 'HA_NUM','STRAHLER', 'SHREVE', 'OS_NAME', 'FNODE_FULL', 'TNODE_FULL', 'NAMENOXML', 'Shape_Length')
        self.t_fc =  os.path.join(self.testing_gdb, 'ne_110m_admin_0_countries')
        self.t_cols =  ('OBJECTID','Shape','ScaleRank','LabelRank','FeatureCla',
                      'SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADMIN',
                      'ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT',
                      'SU_A3','NAME','ABBREV','POSTAL','NAME_FORMA','TERR_',
                      'NAME_SORT','MAP_COLOR','POP_EST','GDP_MD_EST','FIPS_10_',
                      'ISO_A2','ISO_A3','ISO_N3','Shape_Length','Shape_Area')
        pass

    def tearDown(self):
        pass

    def testnames(self):
        est = map(str, tuple(ap.names(self.t_fc)))
        obs = ('OBJECTID','Shape','ScaleRank','LabelRank','FeatureCla',
                'SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADMIN',
                'ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT',
                'SU_A3','NAME','ABBREV','POSTAL','NAME_FORMA','TERR_',
                'NAME_SORT','MAP_COLOR','POP_EST','GDP_MD_EST','FIPS_10_',
                'ISO_A2','ISO_A3','ISO_N3','Shape_Length','Shape_Area')
        self.assertEqual(tuple(est), obs)
        pass

    def testtypes(self):
        est = map(str, tuple(ap.types(self.t_fc)))
        obs = ('OID','Geometry','SmallInteger','SmallInteger','String','String',
                'String','Single','Single','String','String','String','Single',
                'String', 'String','Single','String','String','String','String',
                'String','String', 'String','String','Single','Double','Double',
                'Single','String','String', 'Single','Double','Double')
        pass

    def testnrow(self):
        est = ap.nrow(self.t_fc)
        obs = 177
        self.assertEqual(est, obs)
        pass

##    def testvalues(self):
##        pass
##
##    def testdistinct(self):
##        pass

    def testhead(self):
        est = 5
        hd = ap.head(self.t_fc, est, geoms = " ", verbose=False)
        obs = len(hd[0])
        self.assertEqual(est, obs)
        pass

    def testchart(self):
        obs = r'c:\temp\chart.jpg'
        t_fc = self.t_fc
        est = ap.chart(t_fc, obs, texts = {'txt': 'Element txt'}, openit=False)
        self.assertEqual(est, obs)
        pass

    def testplot(self):
        pic = r'c:\temp\plot.png'
        x = xrange(20)
        ap.plot(x, out_file=pic, openit=False)
        y = xrange(50,70)
        ap.plot(x, y, pic, 'Main', 'X [m]', 'Y [m]', 'o', 'k', openit=False)
        os.remove(pic)
        with self.assertRaises(ap.ArcapiError):
            ap.plot(x, [1,2,3], pic, 'Main', 'X [m]', 'Y [m]', 'o', 'k', openit=False)
        pass

    def testrename_col(self):
        import arcpy
        import tempfile
        owo = arcpy.env.overwriteOutput
        arcpy.env.overwriteOutput = True
        tmpfc = os.path.join(tempfile.gettempdir(), "tmp")
        tmpfc = arcpy.CopyFeatures_management(self.t_fc, tmpfc).getOutput(0)
        est = ap.rename_col(tmpfc, "ABBREV", "ABBREVIATION")
        obs = "ABBREVIATI"
        arcpy.Delete_management(tmpfc)
        arcpy.env.overwriteOutput = owo
        self.assertEqual(est, obs)
        pass

    def testtlist_to_table(self):
        ot = arcpy.CreateScratchName('tmp.dbf', workspace='c:\\temp')
        colnames = ['NAME', 'POP_EST']
        coltypes = ['TEXT', 'DOUBLE']
        collengths = [250, '#']
        coldefs = zip(colnames, coltypes, collengths)

        # read data
        tl = []
        with arcpy.da.SearchCursor(self.t_fc, colnames) as sc:
            for row in sc:
                tl.append(tuple(row))

        # write as table
        ot = ap.tlist_to_table(tl, ot, coldefs, -9, 'nullText')
        ap.head(ot)
        est = int(arcpy.GetCount_management(ot).getOutput(0))
        obs = int(arcpy.GetCount_management(self.t_fc).getOutput(0))

        arcpy.Delete_management(ot)
        self.assertEqual(est, obs)
        pass

##    def testdocu(self):
##        pass

    def testmeta(self):
        fcws = 'c:\\temp'
        fcnm = os.path.basename(arcpy.CreateScratchName('tmp.shp', workspace=fcws))

        fc = arcpy.FeatureClassToFeatureClass_conversion(
            self.t_fc,
            fcws,
            fcnm
        ).getOutput(0)

        ap.meta(fc, 'OVERWRITE', title="Bar")
        ap.meta(fc, 'append', purpose='example', abstract='Column Spam means eggs')

        ap.dlt(fc)
        pass

##    def testmsg(self):
##        pass

    def testfrequency(self):
        est = ap.frequency([1,1,2,3,4,4,4])
        obs = {1: 2, 2: 1, 3: 1, 4: 3}
        samekeys = set(est.keys()) == set(obs.keys())
        good = all([samekeys] + [est[i] == obs[i] for i in est])
        self.assertTrue(good)
        pass

    def testlist_environments(self):
        envs = ap.list_environments([])
        self.assertEqual(len(envs), 50)
        pass

    def testoidF(self):
        est = ap.oidF(self.t_fc)
        obs = "OBJECTID"
        self.assertEqual(str(est), obs)
        pass

    def testshpF(self):
        est = ap.shpF(self.t_fc)
        obs = "Shape"
        self.assertEqual(str(est), obs)
        pass

    def testtstamp(self):
        est = []
        est.append(len(ap.tstamp()) == len('20140216184029'))
        est.append(len(ap.tstamp("lr")) == len('lr20140216184045'))
        est.append(len(ap.tstamp("lr", "%H%M%S")) == len('lr184045'))
        est.append(len(ap.tstamp("lr", "%H%M%S")) == len('lr184045'))
        est.append(len(ap.tstamp("lr", "%H%M%S", s=('run',1))) == len('lr184527_run_1'))
        obs = [True, True, True, True, True]
        self.assertEqual(est, obs)
        pass

    def testdlt(self):
        est = []
        wc = '"OBJECTID" < 11'
        lr = arcpy.management.MakeFeatureLayer(self.t_fc, "lr", wc).getOutput(0)
        # TODO: test for deleting layers won't pass even though ap.dlt works
        #print lr
        #print arcpy.Exists(lr)
        tempfc = 'in_memory\\tmp'
        if arcpy.Exists(tempfc):
            arcpy.Delete_management(tempfc)
        tmpfc = arcpy.CopyFeatures_management(lr, tempfc).getOutput(0)
        fc = arcpy.CopyFeatures_management(tmpfc, arcpy.CreateScratchName("tmp.shp", workspace="c:\\temp")).getOutput(0)
        ap.dlt(lr)
        est.append(ap.dlt(tmpfc))
        est.append(ap.dlt(fc))
        est.append(ap.dlt('this does not exist'))
        self.assertEquals(est, [True, True, False])
        pass

    def testcleanup(self):
        x = []
        out = arcpy.CreateScratchName("tmp", workspace=arcpy.env.scratchGDB)
        x.append(arcpy.management.Copy(self.t_fc, out).getOutput(0))
        est = ap.cleanup(x)
        obs = 0
        self.assertEqual(est, obs)

    def testto_points(self):
        obs = 10
        wc = '"OBJECTID" < ' + str(obs + 1)
        ofc = arcpy.CreateScratchName("tmp_out.shp", workspace="c:\\temp")
        cs = 27700
        ptfc = ap.to_points(self.t_fc, ofc, "POP_EST", "GDP_MD_EST", cs, w = wc)
        est = int(arcpy.GetCount_management(ptfc).getOutput(0))
        arcpy.Delete_management(ptfc)
        self.assertEqual(est, obs)
        pass


##    def testwsp(self):
##        pass
##
##    def testswsp(self):
##        pass

    def testto_scratch(self):
        est = []
        obs = []
        arcpy.env.scratchWorkspace = arcpy.env.scratchGDB
        s = arcpy.env.scratchWorkspace

        est.append(ap.to_scratch('foo', 0))
        obs.append(ap.os.path.join(s, 'foo'))
        est.append(ap.to_scratch('foo', 1))
        obs.append(os.path.join(s, 'foo0'))
        est.append(ap.to_scratch('foo.shp', 0))
        obs.append(os.path.join(s, 'foo_shp'))
        est.append(ap.to_scratch('foo.shp', 1))
        obs.append(os.path.join(s, 'foo_shp0'))

        # not tested for file based workspaces
        arcpy.env.scratchWorkspace = arcpy.env.scratchFolder
        a = arcpy.env.scratchWorkspace
        ap.to_scratch('foo', 0) == os.path.join(s, 'foo')
        ap.to_scratch('foo', 1) == os.path.join(s, 'foo0')
        ap.to_scratch('foo.shp', 0) == os.path.join(s, 'foo_shp')
        ap.to_scratch('foo.shp', 1) == os.path.join(s, 'foo_shp0')

        eq = all([ei == oi for ei,oi in zip(est, obs)])
        self.assertTrue(eq)
    
    def testremap_sa(self):
        est = []

        remapped = ap.remap_3d(10,50,10)
        est.append(remapped == '10 20 1;20 30 2;30 40 3;40 50 4')

        remapped = ap.remap_3d(0,5,1)
        est.append(remapped == '0 1 1;1 2 2;2 3 3;3 4 4;4 5 5')

        remapped = ap.remap_3d(-10,10,5)
        est.append(remapped == '-10 -5 1;-5 0 2;0 5 3;5 10 4')

        remapped = ap.remap_3d(-10,10,-5)
        est.append(remapped == '')

        remapped = ap.remap_3d(10,-20,-7)
        est.append(remapped == '10 3 1;3 -4 2;-4 -11 3;-11 -18 4;-18 -25 5')

        self.assertTrue(all(est))

    def testremap_3d(self):
        est = []

        remapped = ap.remap_sa(10,50,10)
        ob = [[[10, 20], 1], [[20, 30], 2], [[30, 40], 3], [[40, 50], 4]]
        est.append(remapped == ob)

        remapped = ap.remap_sa(0,5,1)
        ob = [[[0, 1], 1], [[1, 2], 2], [[2, 3], 3], [[3, 4], 4], [[4, 5], 5]]
        est.append(remapped == ob)

        remapped = ap.remap_sa(-10,10,5)
        ob = [[[-10, -5], 1], [[-5, 0], 2], [[0, 5], 3], [[5, 10], 4]]
        est.append(remapped == ob)

        remapped = ap.remap_sa(-10,10,-5)
        ob = []
        est.append(remapped == ob)

        remapped = ap.remap_sa(10,-20,-7)
        ob = [
            [[10, 3], 1], [[3, -4], 2], [[-4, -11], 3], [[-11, -18], 4],
            [[-18, -25], 5]
        ]
        est.append(remapped == ob)

        self.assertTrue(all(est))

    def testfind(self):
        self.testingfolder = os.path.join(os.path.dirname(sys.argv[0]), 'testing')
        obs = [1, 5]
        est = []
        findings = ap.find('*.shp', self.testingfolder)
        est.append(len(findings))
        findings = ap.find('*110m*', self.testingfolder)
        est.append(len(findings))
        self.assertEqual(est, obs)

    def testfixArgs(self):
        list_args = 'C:\Temp\Shapefiles\Contours.shp;C:\Temp\Shapefiles\Contours.shp'
        est = ap.fixArgs(list_args, list)
        obs = ['C:\\Temp\\Shapefiles\\Contours.shp', 'C:\\Temp\\Shapefiles\\Contours.shp']
        self.assertEqual(est, obs)
        est = ap.fixArgs('false', bool)
        self.assertEqual(est, False)
        pass

    def testint_to_float(self):
        _dir = os.path.join(self.testingfolder, r'testing_files\rasters')
        ndvi = os.path.join(_dir, 'dh_july_ndvi')
        ob = round(arcpy.Raster(ndvi).maximum, 5)
        int_rst = os.path.join(_dir, 'ndvi_int')
        est = os.path.join(_dir, 'ndvi_tst')
        if arcpy.CheckExtension('Spatial') == 'Available':
            arcpy.CheckOutExtension('Spatial')
            arcpy.sa.Int(arcpy.sa.Times(ndvi, 1000000)).save(int_rst)
            arcpy.CheckInExtension('Spatial')
            ap.int_to_float(int_rst, est, 6)
            self.assertEqual(ob, round(arcpy.Raster(est).maximum, 5))
            for rast in [int_rst, est]:
                try:
                    arcpy.Delete_management(rast)
                except:pass
        pass

    def testfill_no_data(self):
        _dir = os.path.join(self.testingfolder, r'testing_files\rasters')
        ndvi = os.path.join(_dir, 'dh_july_ndvi')
        est = os.path.join(_dir, 'ndvi_fill')
        null = os.path.join(_dir, 'null_rst')
        if arcpy.CheckExtension('Spatial') == 'Available':
            ap.fill_no_data(ndvi, est, 10, 10)
            arcpy.CheckOutExtension('Spatial')
            arcpy.sa.IsNull(est).save(null)
            self.assertEqual(arcpy.Raster(null).maximum, 0)
            arcpy.CheckInExtension('Spatial')
            for rast in [est, null]:
                try:
                    arcpy.Delete_management(rast)
                except:pass
        pass

    def testmeters_to_feet(self):
        _dir = os.path.join(self.testingfolder, r'testing_files\rasters')
        dem = os.path.join(_dir, 'dh30m_dem')
        est = os.path.join(_dir, 'dem_ft')
        ap.meters_to_feet(dem, est)
        self.assertEqual(int(arcpy.Raster(est).maximum), 6244)
        try:
            arcpy.Delete_management(est)
        except:
            pass
        pass

    def testcopy_schema(self):
        tmp = r'in_memory\schema_test'
        ap.copy_schema(self.t_fc, tmp)
        self.assertTrue(arcpy.Exists(tmp))
        arcpy.Delete_management(tmp)
        pass

    def testmake_poly_from_extent(self):
        desc = arcpy.Describe(self.t_fc2)
        ext = desc.extent
        sr = desc.spatialReference
        est = ap.make_poly_from_extent(ext, sr)
        self.assertEqual(str(ext), str(est.extent))
        pass

    def testlist_all_fcs(self):
        est = ap.list_all_fcs(self.testing_gdb, '*', 'All', True)
        obs = ['Illinois', 'ne_110m_admin_0_countries']
        self.assertEqual(est, obs)
        pass

    def testfield_list(self):
        il = os.path.join(self.testing_gdb, 'Illinois')
        est = ap.field_list(il, ['state_fips', 'cnty_fips'])
        obs = ['OBJECTID', 'Shape', 'NAME', 'STATE_NAME',
               'FIPS', 'Shape_Length', 'Shape_Area']
        self.assertEqual(est, obs)
        pass

    def testget_field_type(self):
        il = os.path.join(self.testing_gdb, 'Illinois')
        est = ap.get_field_type('NAME', il)
        self.assertEqual(est, 'TEXT')
        pass

    def testmatch_field(self):
        fc = os.path.join(self.testing_gdb, 'Illinois')
        est = ap.match_field(fc, '*fips', True)
        obs = ['STATE_FIPS', 'CNTY_FIPS', 'FIPS']
        self.assertEqual(est, obs)
        pass

    def testadd_fields_from_table(self):
        fc = os.path.join(self.testing_gdb, 'Illinois')
        copy = fc + '_copy'
        if arcpy.Exists(copy):
            arcpy.Delete_management(copy)
        arcpy.CopyFeatures_management(fc, copy)
        flds = ['POP1990', 'POP2000']
        tab = fc = os.path.join(self.testing_gdb, 'Illinois_county_info')
        ap.add_fields_from_table(copy, tab, flds)
        est = [f.name for f in arcpy.ListFields(copy)]
        try:
            arcpy.Delete_management(copy)
        except: pass
        for f in flds:
            self.assertTrue(f in est)
        pass

    def testcreate_field_name(self):
        fc = os.path.join(self.testing_gdb, 'Illinois')
        est = ap.create_field_name(fc, 'NAME')
        self.assertEqual(est, 'NAME_1')
        pass

    def testcopy_fields_from_table(self):
        if arcpy.Exists(r'in_memory\copy'):
            arcpy.Delete_management(r'in_memory\copy')
        fc = os.path.join(self.testing_gdb, 'Illinois')
        copy = fc + '_copy'
        if arcpy.Exists(copy):
            arcpy.Delete_management(copy)
        arcpy.CopyFeatures_management(fc, copy)
        flds = ['POP1990', 'POP2000']
        tab = fc = os.path.join(self.testing_gdb, 'Illinois_county_info')
        ap.copy_fields_from_table(copy, 'CNTY_FIPS', tab, 'CNTY_FIPS', flds)
        est = [f.name for f in arcpy.ListFields(copy)]
        try:
            arcpy.Delete_management(copy)
        except: pass
        for f in flds:
            self.assertTrue(f in est)
        pass

    def testconcatenate(self):
        est = ap.concatenate(['A','B','C'], '-')
        self.assertEqual(est, 'A-B-C')
        pass

    def testconcatenate_fields(self):
        if arcpy.Exists(r'in_memory\copy'):
            arcpy.Delete_management(r'in_memory\copy')
        fc = os.path.join(self.testing_gdb, 'Illinois')
        copy = fc + '_copy'
        if arcpy.Exists(copy):
            arcpy.Delete_management(copy)
        arcpy.CopyFeatures_management(fc, copy)
        ap.concatenate_fields(copy, 'FULL', 75, ['NAME', 'STATE_NAME'], ' County, ')
        obs = 'Jo Daviess County, Illinois'
        with arcpy.da.SearchCursor(copy, 'FULL') as rows:
            est = rows.next()[0]
        del rows
        try:
            arcpy.Delete_management(copy)
        except: pass
        self.assertEqual(est, obs)
        pass

    def testcreate_pie_chart(self):
        tab = fc = os.path.join(self.testing_gdb, 'Illinois_county_info')
        oid = arcpy.AddFieldDelimiters(tab, arcpy.Describe(tab).OIDFieldName)
        where = '{0} < 11'.format(oid)
        tv = arcpy.MakeTableView_management(tab, 'IL_table', where)
        fig = os.path.join(self.testingfolder, 'IL_county_pop.png')
        # will use 'CNTY_FIPS' as case field since our pop field is
        # already populated for each county
        ap.create_pie_chart(fig, tv, 'NAME','POP2000', 'IL Counties')
        self.assertTrue(os.path.exists(fig))
        try:
            arcpy.Delete_management(fig) # may want to look at the figure, pretty cool!
        except:
            pass
        pass

    def testcombine_pdfs(self):
        _dir = os.path.dirname(self.testingfolder)
        mapDoc = os.path.join(_dir, 'chart.mxd')
        mxd = arcpy.mapping.MapDocument(mapDoc)
        txt_elm = [elm for elm in arcpy.mapping.ListLayoutElements(mxd, 'TEXT_ELEMENT')
                   if elm.text == 'SomeText'][0]
        del_list = []
        for i in range(3):
            txt_elm.text = "Hi, I'm page {0}".format(i)
            pdf = os.path.join(_dir, 'test_{0}.pdf'.format(i))
            arcpy.mapping.ExportToPDF(mxd, pdf, resolution=100)
            del_list.append(pdf)
        combined = os.path.join(_dir, 'combined.pdf')
        del mxd
        ap.combine_pdfs(combined, del_list)
        self.assertTrue(os.path.exists(combined))
        del_list.append(combined)
        try:
            for p in del_list:
                arcpy.Delete_management(p)
        except:
            pass
        pass
if __name__ == '__main__':
    unittest.main(verbosity = 2)
