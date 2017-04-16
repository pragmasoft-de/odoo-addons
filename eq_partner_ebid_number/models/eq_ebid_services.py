# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import requests
import json
from openerp import models, fields, api, _
from openerp.osv import osv
from _ast import TryExcept
    
   
   # def __init__(self, ebid_settings):

#        self._urlMatch = match_service# 'https://matching.unternehmensverzeichnis.org/ws/match/rest/v1.0'
#        self._urlCompany = company_service# 'https://matching.unternehmensverzeichnis.org/ws/company/rest/v1.0/'
    #    self.ebid_settings = ebid_settings
"""
def check_authentication(ebid_settings):
    res = requests.get('https://matching.unternehmensverzeichnis.org/ws/match/rest/v1.0/authorization-test', auth=(ebid_settings.user, ebid_settings.pw))
    if (res.status_code != 200):
        raise osv.except_osv(_('Error'), _('Authentication for EBID failed.'))
"""


def settings_ok(settings):
    return settings and settings.user and settings.pw and settings.urlMatch 
    
def get_ebid_settings(odoo_self):
    config_params = odoo_self.env['ir.config_parameter']
    match_url = config_params.get_param("eq.ebid.service.match.url",False)
    company_url = config_params.get_param("eq.ebid.service.company.url",False)
    homepage_url = config_params.get_param("eq.ebid.homepage.url",False) or 'http://www.unternehmensverzeichnis.org/'
    
    print 'homepage_url: ' + str(homepage_url)
    
    if (company_url and not company_url.endswith('/')):
        company_url += '/'
    if (homepage_url and not homepage_url.endswith('/')):
        homepage_url += '/'
        
    user = config_params.get_param("eq.ebid.user",False)
    pw = config_params.get_param("eq.ebid.pw",False)
    rate_txt = config_params.get_param("eq.ebid.acceptance.rate",False)

    rate = 90
    if (rate_txt):
        rate = int(rate_txt)
    settings = EbidSettings(user, pw, match_url, company_url, homepage_url, rate)   
    return settings
    



def find_company(partner_id, searchParams, ebid_settings):
    header = {'content-type': 'application/json'}
    requestTxt = json.dumps(searchParams)
    try:
        requestRes = requests.post(ebid_settings.urlMatch, data=requestTxt, headers=header, auth=(ebid_settings.user, ebid_settings.pw))
        jsonRes = requestRes.json()
    except Exception, e:
        findCompanyResult = GetEBIDRequestResult(partner_id, "res.partner", None, None, False, 'Error [request findCompany]: ' + e.message, 1, requestTxt,requestRes.text);
        return findCompanyResult
    
    success = False
    foundID = ""
    error = ""
    searchResults = [] #EBIDRequestSearchResult

    respAsText = ''
    if requestRes.status_code == 200:
        success = True
        
        if (jsonRes) and (len(jsonRes) > 0):
            for res in jsonRes:
                foundID = res['ebid']
                rate = res['rate']
                
                rate_arr_txt = ''
                if (res['rateArr']):
                    rate_arr = res['rateArr']
                    if (len(rate_arr) == 14):
                        rate_arr_txt = '{Street: ' + str(rate_arr[7]) + ', ' + 'HouseNo: ' + str(rate_arr[8]) + ', ' + 'City: ' + str(rate_arr[9]) + ', ' + 'Zip: ' + str(rate_arr[10]) + ', ' + 'CompanyName: ' + str(rate_arr[12]) + '}'
                    else:
                        rate_arr_conv = (str(sub_rate) for sub_rate in rate_arr)
                        rate_arr_txt = '{' + ','.join(rate_arr_conv) + '}'
                    
                respAsText +=  '[EBID: ' + str(foundID)+ ', Rate: ' + str(rate) + ', Rate_Arr: ' + rate_arr_txt + ']; '
                
                searchResultItem = EBIDRequestSearchResult(success, "", foundID, rate, rate_arr_txt, rate > ebid_settings.acceptance_rate)
                searchResults.append(searchResultItem)
        else:
            error = "No result found"
    else:
        respAsText = requestRes.text
        if (len(jsonRes) > 0):
            error =  jsonRes['ErrorMessage']
        else:
            error = "Error" #Todo
    findCompanyResult = GetEBIDRequestResult(partner_id, "res.partner", searchResults, None, success, error, 1, requestTxt,respAsText);#requestRes.text)
    
    return findCompanyResult

def get_company_for_ebid(partner_id, ebid, ebid_settings):
    header = {'content-type': 'application/json'}  
    try:
        requestRes = requests.get(ebid_settings.urlCompany + ebid, headers=header, auth=(ebid_settings.user, ebid_settings.pw))
        jsonRes = requestRes.json()
    except Exception, e:
        findCompanyResult = GetEBIDRequestResult(partner_id, "res.partner", None, None, False, 'Error [request get_company_for_ebid]: ' + e.message, 1, 'ebid: ' + ebid,requestRes.text);
        return findCompanyResult
     
    error = ''
    respAsText = ''
    success = False
    if requestRes.status_code == 200:
        success = True
        if (jsonRes) and (len(jsonRes) > 0):
            search_res = SearchForEBIDResult(ebid, jsonRes)
            
    else:
        respAsText = requestRes.text
        if (len(jsonRes) > 0):
            error =  jsonRes['ErrorMessage']
    
    search_ebid_result = GetEBIDRequestResult(partner_id, "res.partner", None, search_res, success, error, 2, '',respAsText);
    
    return search_ebid_result
        
class request_result_info:
    def __init__(self, success, result_count, message, res_id = 0):      
        self.success = success
        self.result_count = result_count
        self.message = message
        self.res_id = res_id
        
class EbidSettings:
    
    def __init__(self, user, pw, matchUrl, companyUrl, homepage, acceptance_rate = 90):
        self.user = user
        self.pw = pw 
        self.urlMatch = matchUrl
        self.urlCompany = companyUrl
        self.homepage = homepage
        self.acceptance_rate = acceptance_rate
        
class GetEBIDRequestResult:
    def __init__(self, res_id, model, resultList, ebid_search_result, success, errorMsg, request_type, request="", response=""):
        self.res_id = res_id
        self.searchHits = resultList
        self.requestOK = success
        self.error = errorMsg
        self.request = request
        self.response = response
        self.model = model
        self.request_type = request_type
        self.ebid_search_result = ebid_search_result
        

class EBIDRequestSearchResult:
    
    def __init__(self, success, errorMsg, ebidno, rate = 0, arr_rate = '', above_rate = False):
        self.requestOK = success
        self.error = errorMsg
        self.ebid_no = ebidno
        self.rate = rate
        self.arr_rate = arr_rate
        
class SearchForEBIDResult:
    
    def __init__(self, ebidno, values):
        self.ebid_no = ebidno
        if (values):
            self.company_name = values['companyName']
            self.street = values['street']
            self.house_no = values['houseNo']
            self.city = values['city']
            self.city_part = values['cityPart']
            self.zip = values['zip']
            self.country = values['country']
            self.phone = values['phone']     
            self.fax = values['fax']     
            self.mobile = values['mobile']     
            self.email = values['email']     
            self.url = values['url']             
            self.ustid_nr = values['ustIdNr']  
            
        