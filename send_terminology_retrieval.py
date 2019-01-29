#!/usr/bin/env python3

import sys
import argparse
import configparser
import urllib.request
import os
import logging
import xml.etree.ElementTree as ET
import networkx
import obonet


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

parser=argparse.ArgumentParser()
parser.add_argument('-p', help='Path Parameters')
args=parser.parse_args()
parameters={}
if __name__ == '__main__':
    import send_terminology_retrieval
    parameters = send_terminology_retrieval.ReadParameters(args)     
    send_terminology_retrieval.Main(parameters)

send_domain =    {
  "BW": "BODY_WEIGHT_DOMAIN",
  "BH": "BEHAVIORAL_DOMAIN",
  "BG": "BODY_WEIGHT_GAIN_DOMAIN",
  "CL": "CLINICAL_DOMAIN",
  "CO": "COMMENTS_DOMAIN",
  "CV": "CARDIOVASCULAR_DOMAIN",
  "DD": "DEATH_DIAGNOSIS_DOMAIN",
  "DM": "DEMOGRAPHICS_DOMAIN",
  "DS": "DISPOSITION_DOMAIN",
  "EG": "ECG_DOMAIN",
  "EX": "EXPOSURE_DOMAIN",
  "FE": "FERTILITY_DOMAIN",
  "FM": "FETAL_DOMAIN",
  "FW": "FOOD_WATER_CONSUMPTION_DOMAIN",
  "FX": "FETAL_PATOLOGY_FINDINGS_DOMAIN",
  "IC": "IMPLANTATION_CLASSIFICATION_DOMAIN",
  "LB": "LABORATORY_FINDINGS_DOMAIN",
  "LR": "CESARIAN_SECTION_DELIVERY_LITTER_DOMAIN",
  "MA": "MACROSCOPIC_FINDINGS_DOMAIN",
  "MI": "MICROSCOPIC_FINDINGS_DOMAIN",
  "NV": "NERVOUS_SYSTEM_DOMAIN",
  "OM": "ORGAN_MEASUREMENT_DOMAIN",
  "PA": "PARING_EVENTS_DOMAIN",
  "PC": "PHARMACOKINETIC_CONCENTRATION_DOMAIN",
  "PM": "PALPABLE_MASSES_DOMAIN",
  "PP": "PHARMACOKINETICS_PARAMETERS_DOMAIN",
  "PY": "NONCLINICAL_PREGNANCY_DOMAIN",
  "RE": "RESPIRATORY_FINDINGS_DOMAIN",
  "SC": "SUBJECT_CHARACTERISTICS_DOMAIN",
  "SE": "SUBJECT_ELEMENTS_DOMAIN",
  "SJ": "SUBJECT_STAGES_DOMAIN",
  "TA": "TRIAL_ARMS_DOMAIN",
  "TE": "TRIAL_ELEMENTS_DOMAIN",
  "TF": "TUMOR_FINDINGS_DOMAIN",
  "TP": "TRIAL_PATHS_DOMAIN",
  "TS": "TRIAL_SUMMARY_DOMAIN",
  "TT": "TRIAL_STAGES_DOMAIN",
  "TX": "TRIAL_SETS_DOMAIN",
  "VS": "VITAL_SIGNS_DOMAIN",
  "NORMAL": "NO_TREATMENT_RELATED_EFFECT_DETECTED"
}
#tengo que codificar la busqueda del primer padre que se encuenre en este diccionario para mapear con SEND
etox_to_send_domain =    {
  "ILO:0000002": "FW",
  "ILO:0000038": "FW",
  "ILO:0000007": "RE",
  "ILO:0000009": "BH",
  "ILO:0000029": "BW",
  "ILO:0000012": "FX",
  "ILO:0000017": "FE",
  "ILO:0000029": "BW",
  "ILO:0000053": "CV",
  "ILO:0000053": "CV",
  "ILO:0000060":"EG",
  "ILO:0000092":"BG",
  "ILO:0000167":"DD",
  "ILO:0000365":"DD",
  "ILO:0000400":"DD",
  "ILO:0000130":"CL",
  "ILO:0000074":"CL",
  "ILO:0000027":"CL",
  "ILO:0000210":"CL",
  "ILO:0000056":"CL",
  "ILO:0000117":"CL",
  "ILO:0000221":"CL",
  "ILO:0000021":"CL",
  "ILO:0000224":"CL",
  "ILO:0000004":"CL",
  "ILO:0000019":"CL",
  "ILO:0000066":"CL",
  "ILO:0000015":"CL",
  "ILO:0000035":"CL",
  "ILO:0000469":"CL",
  "ILO:0000564":"CL",
  "ILO:0000653":"CL",
  "ILO:0000679":"CL",
  "ILO:0000186":"CL",
  "ILO:0000428":"NORMAL" 
}




def ReadParameters(args):
    if(args.p!=None):
        Config = configparser.RawConfigParser()
        Config.read(args.p)
        parameters['output']=Config.get('MAIN', 'output')
       
        parameters['send_terminology_cdisc_url']=Config.get('MAIN', 'send_terminology_cdisc_url')
        parameters['cdisc_send_terminology_dict_output']=Config.get('MAIN', 'cdisc_send_terminology_dict_output')
        
        parameters['etox_send_codelists']=Config.get('MAIN', 'etox_send_codelists')
        parameters['etox_send_codelist_terms']=Config.get('MAIN', 'etox_send_codelist_terms')
        parameters['etox_send_codelist_synonyms']=Config.get('MAIN', 'etox_send_codelist_synonyms')
        
        parameters['etox_anatomy']=Config.get('MAIN', 'etox_anatomy')
        parameters['etox_anatomy_dict_output']=Config.get('MAIN', 'etox_anatomy_dict_output')
        
        
        parameters['etox_moa']=Config.get('MAIN', 'etox_moa')
        
        parameters['etox_moa_dict_output']=Config.get('MAIN', 'etox_moa_dict_output')
        
        parameters['etox_in_life_obs']=Config.get('MAIN', 'etox_in_life_obs')
        parameters['etox_in_life_obs_dict_output']=Config.get('MAIN', 'etox_in_life_obs_dict_output')
        
        
        
        parameters['etox_send_terminology_dict_output']=Config.get('MAIN', 'etox_send_terminology_dict_output')
        
    else:
        logging.error("Please send the correct parameters config.properties --help ")
        sys.exit(1)
    return parameters   



def Main(parameters):
    output=parameters['output']
    
    if not os.path.exists(output):
        os.makedirs(output)
    
    send_terminology_cdisc_url = parameters['send_terminology_cdisc_url']
    cdisc_send_terminology_dict_output=parameters['cdisc_send_terminology_dict_output']
    
    etox_send_codelists = parameters['etox_send_codelists']
    etox_send_codelist_terms = parameters['etox_send_codelist_terms']
    etox_send_codelist_synonyms = parameters['etox_send_codelist_synonyms']
    
    etox_anatomy = parameters['etox_anatomy']
    etox_anatomy_dict_output = parameters['etox_anatomy_dict_output']
    
    etox_moa = parameters['etox_moa']
    etox_moa_dict_output = parameters['etox_moa_dict_output']
   
    etox_in_life_obs = parameters['etox_in_life_obs']
    etox_in_life_obs_dict_output = parameters['etox_in_life_obs_dict_output']
    etox_send_terminology_dict_output = parameters['etox_send_terminology_dict_output']
    
    generate_send_etox_corpus(etox_send_codelists, etox_send_codelist_terms, etox_send_codelist_synonyms, etox_send_terminology_dict_output)
    
    generate_anatomy_etox_corpus(etox_anatomy, etox_anatomy_dict_output)
    generate_moa_etox_corpus(etox_moa, etox_moa_dict_output)
    generate_in_life_observation_etox_corpus(etox_in_life_obs, etox_in_life_obs_dict_output)
    
    outputFileSEND = output+"/send_terminology_search.xml"
    
    download_send_cdis_terminology(send_terminology_cdisc_url, outputFileSEND)
    generate_send_cdis_corpus(outputFileSEND, cdisc_send_terminology_dict_output)

def generate_in_life_observation_etox_corpus(etox_in_life_obs, dict_path):
    logging.info("generate_in_life_observation_etox_corpus  " )
    with open(dict_path,'w') as dict: 
        dict.write('KEYWORD\tLABEL\tTERM_ID\tKEYWORD_TYPE\tSYNONYM_DAT\tIS_A\tIS_PART_OF\tSEND_DOMAIN_CODE\tSEND_DOMAIN_DESC\n')
        graph = obonet.read_obo(etox_in_life_obs)
        id_to_name = {id_: data for id_, data in graph.nodes(data=True)}
        for node in graph.nodes(data=True):
            id = node[0]
            data = node[1]
            name = data['name']
            is_a = ""
            if('is_a' in data):
                is_a = data['is_a']
            relationship=""
            if('relationship' in data):
                relationship = data['relationship'] 
                
            parents = networkx.descendants(graph, id)
            sdomain = etox_to_send_domain.get(id)
            if(sdomain is None): #look for nearest parent in the send_domain dict
                for id_parent in parents:
                    sdomain = etox_to_send_domain.get(id_parent)    
                    if(sdomain is not None):
                        break
            if(sdomain is None):
                sdomain = ''
            sdomain_desc = ''
            label = 'IN_LIFE_OBSERVATION'
            if (sdomain!=''):
                sdomain_desc = send_domain.get(sdomain) 
                label=sdomain_desc
                if(sdomain_desc is None):
                    sdomain_desc = ''
                    label = 'IN_LIFE_OBSERVATION'
                    
            dict.write(name+'\t'+label+'\t'+id+'\tNAME\t\t'+("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\t'+sdomain+'\t'+sdomain_desc+'\n')    
            if('synonym' in data):
                synonyms = data['synonym']
                for syn in synonyms:
                    syn_term = syn[syn.index('"')+1:syn.rindex('"')]
                    syn_dat = syn[syn.rindex('"')+2:]
                    dict.write(syn_term+'\t'+label+'\t'+id+'\tSYNONYM\t'+syn_dat+'\t'+ ("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\t'+sdomain+'\t'+sdomain_desc+'\n')    
                    dict.flush()
            dict.flush()   
    logging.info(" Process end" )
    
def getStutyDomain(node):
    id = node[0]
    send_domain = etox_to_send_domain.get(id)    
    if(send_domain is None):
        data = node[1]
        if('is_a' in data):
            is_a = data['is_a']
            getStutyDomain()
        else:
            return ""
        
        
def generate_anatomy_etox_corpus(etox_anatomy, dict_path):
    logging.info("generate_anatomy_etox_corpus  " )
    with open(dict_path,'w') as new_result:
        new_result.write('KEYWORD\tLABEL\tTERM_ID\tKEYWORD_TYPE\tSYNONYM_DAT\tIS_A\tIS_PART_OF\n')
        graph = obonet.read_obo(etox_anatomy)
        for node in graph.nodes(data=True):
            id = node[0]
            data = node[1]
            name = data['name']
            is_a = ""
            if('is_a' in data):
                is_a = data['is_a']
            relationship=""
            if('relationship' in data):
                relationship = data['relationship']    
            new_result.write(name+'\tANATOMY\t'+id+'\tNAME\t\t'+("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\n')
            if('synonym' in data):
                synonyms = data['synonym']
                for syn in synonyms:
                    syn_term = syn[syn.index('"')+1:syn.rindex('"')]
                    syn_dat = syn[syn.rindex('"')+2:]
                    new_result.write(syn_term+'\tANATOMY\t'+id+'\tSYNONYM\t'+syn_dat+'\t'+ ("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\n' )
                    new_result.flush()
                    
            new_result.flush()   
            
            
    logging.info(" Process end" )
def generate_moa_etox_corpus(etox_moa, dict_path):
    logging.info("generate_moa_etox_corpus  " )
    with open(dict_path,'w') as new_result: 
        new_result.write('KEYWORD\tLABEL\tTERM_ID\tKEYWORD_TYPE\tSYNONYM_DAT\tIS_A\tIS_PART_OF\n')
        graph = obonet.read_obo(etox_moa)
        for node in graph.nodes(data=True):
            id = node[0]
            data = node[1]
            name = data['name']
            is_a = ""
            if('is_a' in data):
                is_a = data['is_a']
            relationship=""
            if('relationship' in data):
                relationship = data['relationship']    
            new_result.write(name+'\tMOA\t'+id+'\tNAME\t\t'+("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\n')
            if('synonym' in data):
                synonyms = data['synonym']
                for syn in synonyms:
                    syn_term = syn[syn.index('"')+1:syn.rindex('"')]
                    syn_dat = syn[syn.rindex('"')+2:]
                    new_result.write(syn_term+'\tMOA\t'+id+'\tSYNONYM\t'+syn_dat+'\t'+ ("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\n' )
                    new_result.flush()
            new_result.flush()   
                   
        
    logging.info(" Process end" )


def generate_send_etox_corpus(etox_send_codelists, etox_send_codelist_terms, etox_send_codelist_synonyms, dict_path):
    logging.info("generate_send_etox_corpus  " )
    with open(etox_send_codelists,'r') as code_list: 
        with open(etox_send_codelist_terms,'r') as terms:
            with open(etox_send_codelist_synonyms,'r') as synonyms:
                with open(dict_path,'w') as new_result: 
                    new_result.write('KEYWORD\tLABEL\tCODELIST_ID\tTERM_ID\tKEYWORD_TYPE\tTERM_NAME\tSYNONYM_TYPE\tSOURCE\n')
                    new_result.flush()
                    for line_codelist in code_list:
                        data_codelist = line_codelist.split('\t')
                        if(data_codelist[0]!='CODELIST_ID'):
                            terms.seek(0)
                            for line_term in terms:
                                data_term = line_term.split('\t')
                                if(data_codelist[0]==data_term[0] and data_codelist[0]!='CODELIST_ID'):
                                    new_result.write(data_term[2] + '\t' + data_codelist[2] + '\t' + data_term[0] + '\t' + data_term[1] + '\tPRIMARY' +'\t\t\t\n' )
                                    new_result.flush()
                                    
                                    synonyms.seek(0)
                                    for line_syn in synonyms:
                                        data_syn = line_syn.split('\t')
                                        if(data_syn[1]==data_term[1] and data_syn[0]!='CODELIST_ID'):
                                            new_result.write(data_syn[2] + '\t' + data_codelist[2] + '\t' + data_term[0] + '\t' + data_term[1] + '\tSYNONYM' + '\t' + data_term[2] + '\t' + data_syn[3] + '\t' + data_syn[4])
                                    new_result.flush()   
                                    
                            
                            
    logging.info(" Process end" )

def download_send_cdis_terminology(send_terminology_url, outputFile):
    logging.info("Downloading SEND Terminology from : " + send_terminology_url )
    url = send_terminology_url
    #request = urllib.request.Request(url)
    response = urllib.request.urlopen(url)
    response_cyps = response.read()
    with open(outputFile,'wb') as result: 
        result.write(response_cyps)
        result.flush()
    logging.info("Download End ")  

def generate_send_cdis_corpus(unputUniprotFile, outputFile):
    logging.info("generate_send_cdisc_corpus " )
    name_space = "{http://www.cdisc.org/ns/odm/v1.3}"
    nciodm_name_space="{http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC}"
    docXml = ET.parse(unputUniprotFile)
    root = docXml.getroot()
    with open(outputFile,'w') as new_result: 
        new_result.write('KEYWORD\tLABEL\tSUB_LABEL\tOID\tEXT_CODE_ID\tKEYWORD_TYPE\n')
        study_xml = root.find(name_space+"Study")
        metadataversion_xml = study_xml.find(name_space+"MetaDataVersion")
        for entry in metadataversion_xml.findall(name_space+"CodeList"):
            try:
                oid=entry.attrib.get("OID")
                oid_i = oid.rfind('.')
                oid=oid[oid_i+1:]
                code_list_name = entry.attrib.get("Name")
                code_list_name = code_list_name.upper()
                for item in entry.findall(name_space+"EnumeratedItem"):
                    code = item.attrib.get("CodedValue")
                    if (send_domain.get(code) is not None):
                        code = send_domain.get(code)
                    nciodm_ExtCodeID = item.attrib.get(nciodm_name_space+"ExtCodeID")
                    for syn in item.findall(nciodm_name_space+"CDISCSynonym"):
                        new_result.write(syn.text+'\t'+ oid+'_'+code_list_name +'\t' + code.replace(" ","_") +'\t'+ oid +'\t'+ nciodm_ExtCodeID +'\t'+ 'SYNONYM'+'\n')
                    nciodm_PreferredTerm=item.find(nciodm_name_space+"PreferredTerm")   
                    new_result.write(nciodm_PreferredTerm.text+'\t'+ oid+'_'+code_list_name +'\t' +code.replace(" ","_") +'\t'+ oid +'\t'+ nciodm_ExtCodeID +'\t'+ 'PRIMARY'+'\n')
                    new_result.flush()
            except Exception as inst:
                logging.error("Error reading" + entry.find(name_space+"name").text)  
                logging.error(str(inst))  
    logging.info(" Process end" )




