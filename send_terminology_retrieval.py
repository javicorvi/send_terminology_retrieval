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

codelist_id_dictionary ={};

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
  "NORMAL": "NO_TREATMENT_RELATED_EFFECT_DETECTED",
  "ANIMAL_IDENTIFICATION_FINDING": "ANIMAL_IDENTIFICATION_FINDING",
  "DOSING_FINDING": "DOSING_FINDING"
}
#tengo que codificar la busqueda del primer padre que se encuenre en este diccionario para mapear con SEND
etox_to_send_domain =    {
  "ILO:0000002": "FW", # food consumption
  "ILO:0000038": "FW", # water consumption
  "ILO:0000007": "RE", # breathing
  "ILO:0000009": "BH", # general behaviour
  "ILO:0000029": "BW", # bodyweight/growth
  "ILO:0000012": "FX", # feces/urine
  "ILO:0000017": "FE", # reproductive finding
  "ILO:0000053": "CV", # cardiovascular parameter
  "ILO:0000060":"EG", # ecg
  "ILO:0000092":"BG", # bodyweight increase
  "ILO:0000167":"DD", # dead (more diagnosis)
  "ILO:0000365":"DD", # killed DD or CL
  "ILO:0000400":"CL", # moribund condition DD or CL
  "ILO:0000130":"CL", # body temperature
  "ILO:0000074":"CL", # eye
  "ILO:0000027":"CL", # mouth
  "ILO:0000210":"CL", # teeth
  "ILO:0000056":"CL", # locomotive behaviour
  "ILO:0000117":"CL", # nose
  "ILO:0000221":"CL", # tongue
  "ILO:0000021":"CL", # skin/fur
  "ILO:0000019":"CL", # administration/collection site
  "ILO:0000066":"CL", # ear
  "ILO:0000015":"CL", # posture
  "ILO:0000035":"CL", # general condition
  "ILO:0000032":"CL", # reflexes
  "ILO:0000041":"CL", # anus 
  "ILO:0000045":"CL", # tail
  "ILO:0000078":"CL", # pulmonary parameter
  "ILO:0000080":"CL", # cage/bleeding
  "ILO:0000191":"CL", # digit/claw
  "ILO:0000195":"CL", # unclasified
  "ILO:0000685":"CL", # whiskers
  "ILO:0000004":"CL", # varia
  "ILO:0000428":"NORMAL", # normal as no finding detected
  "ILO:0000067" : "ANIMAL_IDENTIFICATION_FINDING" , #animal identification not mapped as finding 
  "ILO:0000084" : "DOSING_FINDING"  #dosing not mapped findings regarding the dosis
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
        
        parameters['umls_terminology_path']=Config.get('MAIN', 'umls_terminology_path')
        parameters['umls_terminology_dict_path']=Config.get('MAIN', 'umls_terminology_dict_path')
        
        
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
    
    outputFileSEND = output+"/send_terminology_search.xml"
    
    download_send_cdis_terminology(send_terminology_cdisc_url, outputFileSEND)
    generate_send_cdis_corpus(outputFileSEND, cdisc_send_terminology_dict_output)
    
    generate_send_etox_corpus(etox_send_codelists, etox_send_codelist_terms, etox_send_codelist_synonyms, etox_send_terminology_dict_output)
    generate_anatomy_etox_corpus(etox_anatomy, etox_anatomy_dict_output)
    generate_moa_etox_corpus(etox_moa, etox_moa_dict_output)
    generate_in_life_observation_etox_corpus(etox_in_life_obs, etox_in_life_obs_dict_output)
    
    convert_to_gate_gazetter(etox_send_terminology_dict_output, etox_send_terminology_dict_output.replace(".txt",".lst"))
    convert_to_gate_gazetter(etox_anatomy_dict_output, etox_anatomy_dict_output.replace(".txt",".lst"))
    convert_to_gate_gazetter(etox_moa_dict_output, etox_moa_dict_output.replace(".txt",".lst"))
    convert_to_gate_gazetter(etox_in_life_obs_dict_output, etox_in_life_obs_dict_output.replace(".txt",".lst"))
    convert_to_gate_gazetter(cdisc_send_terminology_dict_output, cdisc_send_terminology_dict_output.replace(".txt",".lst"))

    
def generate_in_life_observation_etox_corpus(etox_in_life_obs, dict_path):
    logging.info("generate_in_life_observation_etox_corpus  " )
    terms_list = []
    with open(dict_path,'w') as dict: 
        dict.write('INTERNAL_CODE\tKEYWORD\tLABEL\tETOX_TERM_ID\tETOX_KEYWORD_TYPE\tETOX_SYNONYM_DAT\tETOX_IS_A\tETOX_IS_PART_OF\tETOX_SEND_DOMAIN_CODE\tETOX_SEND_DOMAIN_DESC\n')
        graph = obonet.read_obo(etox_in_life_obs)
        internal_code = 1
        id_to_name = {id_: data for id_, data in graph.nodes(data=True)}
        for node in graph.nodes(data=True):
            id = node[0]
            data = node[1]
            name = data['name'].lower()
            is_a = " "
            if('is_a' in data):
                is_a = data['is_a']
            relationship=" "
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
                sdomain = ' '
            sdomain_desc = ' '
            label = 'IN_LIFE_OBSERVATION'
            if (sdomain!=' '):
                sdomain_desc = send_domain.get(sdomain) 
                label=sdomain_desc
                if(sdomain_desc is None):
                    sdomain_desc = ' '
                    label = 'IN_LIFE_OBSERVATION'
            if(name not in terms_list):
                terms_list.append(name)
                #dict.write(str(internal_code) +'\t'+name+'\t'+label+'\t'+id+'\tNAME\t \t'+("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\t'+sdomain+'\t'+sdomain_desc+'\n')
                dict.write(str(internal_code) +'\t'+name+'\t'+label+'\t'+id+'\tNAME\t \t'+("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\t'+sdomain+'\t'+sdomain_desc+'\n')    
                internal_code = internal_code + 1
            if('synonym' in data):
                synonyms = data['synonym']
                for syn in synonyms:
                    syn_term = syn[syn.index('"')+1:syn.rindex('"')].lower()
                    syn_dat = syn[syn.rindex('"')+2:]
                    if(syn_term not in terms_list):
                        terms_list.append(syn_term)
                        #dict.write(str(internal_code) +'\t'+syn_term+'\t'+label+'\t'+id+'\tSYNONYM\t'+syn_dat+'\t'+ ("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\t'+sdomain+'\t'+sdomain_desc+'\n')
                        dict.write(str(internal_code) +'\t'+syn_term+'\t'+label+'\t'+id+'\tSYNONYM\t'+syn_dat+'\t'+ ("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\t'+sdomain+'\t'+sdomain_desc+'\n')    
                        dict.flush()
                        internal_code = internal_code + 1
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
    terms_list = []
    with open(dict_path,'w') as new_result:
        new_result.write('INTERNAL_CODE\tKEYWORD\tLABEL\tETOX_TERM_ID\tETOX_KEYWORD_TYPE\tETOX_SYNONYM_DAT\tETOX_IS_A\tETOX_IS_PART_OF\n')
        graph = obonet.read_obo(etox_anatomy)
        internal_code = 1
        for node in graph.nodes(data=True):
            id = node[0]
            data = node[1]
            name = data['name'].lower()
            is_a = " "
            if('is_a' in data):
                is_a = data['is_a']
            relationship=" "
            if('relationship' in data):
                relationship = data['relationship']
            
            if('synonym' in data):
                synonyms = data['synonym']
                for syn in synonyms:
                    syn_term = syn[syn.index('"')+1:syn.rindex('"')].lower()
                    syn_dat = syn[syn.rindex('"')+2:]
                    if(syn_term not in terms_list):
                        terms_list.append(syn_term)
                        new_result.write(str(internal_code) +'\t'+syn_term+'\tANATOMY\t'+id+'\tSYNONYM\t'+syn_dat+'\t'+ ("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\n' )
                        internal_code = internal_code + 1
                        new_result.flush()
            
            if(name not in terms_list):
                terms_list.append(name)    
                new_result.write(str(internal_code) +'\t'+name+'\tANATOMY\t'+id+'\tNAME\t \t'+("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\n')
                internal_code = internal_code + 1
            
            
                    
            new_result.flush()   
            
            
    logging.info(" Process end" )
def generate_moa_etox_corpus(etox_moa, dict_path):
    logging.info("generate_moa_etox_corpus  " )
    terms_list = []
    with open(dict_path,'w') as new_result: 
        new_result.write('INTERNAL_CODE\tKEYWORD\tLABEL\tETOX_TERM_ID\tETOX_KEYWORD_TYPE\tETOX_SYNONYM_DAT\tETOX_IS_A\tETOX_IS_PART_OF\n')
        graph = obonet.read_obo(etox_moa)
        internal_code = 1
        for node in graph.nodes(data=True):
            id = node[0]
            data = node[1]
            name = data['name'].lower()
            is_a = " "
            if('is_a' in data):
                is_a = data['is_a']
            relationship=" "
            if('relationship' in data):
                relationship = data['relationship']    
            
            if(name not in terms_list):
                terms_list.append(name)
                new_result.write(str(internal_code) +'\t'+name+'\tMOA\t'+id+'\tNAME\t \t'+("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\n')
                internal_code = internal_code + 1
            if('synonym' in data):
                synonyms = data['synonym']
                for syn in synonyms:
                    syn_term = syn[syn.index('"')+1:syn.rindex('"')].lower()
                    syn_dat = syn[syn.rindex('"')+2:]
                    if(syn_term not in terms_list):
                        terms_list.append(syn_term)
                        new_result.write(str(internal_code) +'\t'+syn_term+'\tMOA\t'+id+'\tSYNONYM\t'+syn_dat+'\t'+ ("-".join(str(x) for x in is_a))+'\t'+("-".join(str(x) for x in relationship))+'\n' )
                        internal_code = internal_code + 1
                        new_result.flush()
            new_result.flush()   
    logging.info(" Process end" )


def generate_send_etox_corpus(etox_send_codelists, etox_send_codelist_terms, etox_send_codelist_synonyms, dict_path):
    logging.info("generate_send_etox_corpus  " )
    terms_list = []
    with open(etox_send_codelists,'r') as code_list: 
        with open(etox_send_codelist_terms,'r') as terms:
            with open(etox_send_codelist_synonyms,'r') as synonyms:
                with open(dict_path,'w') as new_result: 
                    new_result.write('INTERNAL_CODE\tKEYWORD\tLABEL\tETOX_CODELIST\tETOX_CODELIST_ID\tETOX_SEND_CODE_ID\tETOX_SEND_CODE\tETOX_KEYWORD_TYPE\tETOX_TERM_NAME\tETOX_SYNONYM_TYPE\tETOX_SOURCE\n')
                    new_result.flush()
                    internal_code = 1
                    for line_codelist in code_list:
                        data_codelist = line_codelist.split('\t')
                        if(data_codelist[0]!='CODELIST_ID'):
                            terms.seek(0)
                            for line_term in terms:
                                data_term = line_term.split('\t')
                                if(data_codelist[0]==data_term[0] and data_codelist[0]!='CODELIST_ID'):
                                    if(data_term[2].lower() not in terms_list):
                                        terms_list.append(data_term[2].lower())    
                                        etox_send_code = ''
                                        if(data_term[0]=='C67154'):
                                            data_term[0]='C65047' 
                                        if data_term[0]+"_"+data_term[1] in codelist_id_dictionary:
                                            etox_send_code = codelist_id_dictionary[data_term[0]+"_"+data_term[1]]
                                        new_result.write(str(internal_code) +'\t'+data_term[2].lower() + '\t' + data_codelist[2] + '\t' + data_codelist[2] + '\t' + data_term[0] + '\t' + data_term[1] + '\t' +etox_send_code + '\tPRIMARY' +'\t\t\t\n' )
                                        new_result.flush()
                                        internal_code = internal_code + 1
                                    synonyms.seek(0)
                                    for line_syn in synonyms:
                                        data_syn = line_syn.split('\t')
                                        if(data_syn[1]==data_term[1] and data_syn[0]!='CODELIST_ID'):
                                            if(data_syn[2].lower() not in terms_list):
                                                terms_list.append(data_syn[2].lower()) 
                                                new_result.write(str(internal_code) +'\t'+data_syn[2].lower() + '\t' + data_codelist[2] + '\t' + data_codelist[2] + '\t' + data_term[0] + '\t' + data_term[1] + '\t' + etox_send_code + '\tSYNONYM' + '\t' + data_term[2] + '\t' + data_syn[3]+ '\t' + data_syn[4])
                                                internal_code = internal_code + 1
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
    terms_list = []
    name_space = "{http://www.cdisc.org/ns/odm/v1.3}"
    nciodm_name_space="{http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC}"
    docXml = ET.parse(unputUniprotFile)
    root = docXml.getroot()
    with open(outputFile,'w') as new_result: 
        new_result.write('INTERNAL_CODE\tKEYWORD\tLABEL\tCDISC_SEND_CODE\tCDISC_CODELIST\tCDISC_SEND_CODE_ID\tCDISC_CODELIST_NAME\tCDISC_KEYWORD_TYPE\tCDISC_CODELIST_ID\tCDISC_CODELIST_LINK\n')
        study_xml = root.find(name_space+"Study")
        metadataversion_xml = study_xml.find(name_space+"MetaDataVersion")
        internal_code = 1
        for entry in metadataversion_xml.findall(name_space+"CodeList"):
            try:
                oid=entry.attrib.get("OID")
                link=oid
                oid_i = oid.rfind('.')
                oid=oid[oid_i+1:]
                oid_codelist = entry.attrib.get(nciodm_name_space+"ExtCodeID")
                code_list_name = entry.attrib.get("Name")
                code_list_name = code_list_name.upper()
                for item in entry.findall(name_space+"EnumeratedItem"):
                    code = item.attrib.get("CodedValue").replace(" ","_")
                    '''if (send_domain.get(code) is not None):
                        code = send_domain.get(code)'''
                    code = code.replace(" ","_")    
                    nciodm_ExtCodeID = item.attrib.get(nciodm_name_space+"ExtCodeID")
                    codelist_id_dictionary[oid_codelist+"_"+nciodm_ExtCodeID] = item.attrib.get("CodedValue")
                    label = oid+'_'+item.attrib.get("CodedValue")+'_'+code_list_name
                    #label = oid
                    for syn in item.findall(nciodm_name_space+"CDISCSynonym"):
                        if(syn.text.lower() not in terms_list):
                            terms_list.append(syn.text.lower())
                            new_result.write(str(internal_code) +'\t'+ syn.text.lower()+'\t'+ label +'\t' + code +'\t'+ oid +'\t'+ nciodm_ExtCodeID +'\t'+ code_list_name +'\t'+ 'SYNONYM'+'\t'+ oid_codelist +'\t'+ link +'\n')
                            internal_code = internal_code + 1
                    nciodm_PreferredTerm=item.find(nciodm_name_space+"PreferredTerm") 
                    term = nciodm_PreferredTerm.text.lower()
                    if(term not in terms_list):
                        terms_list.append(term)    
                        new_result.write(str(internal_code) +'\t'+term+'\t'+ label +'\t' +code +'\t'+ oid +'\t'+ nciodm_ExtCodeID +'\t'+ code_list_name +'\t'+ 'PRIMARY'+'\t'+ oid_codelist +'\t'+ link +'\n')
                        internal_code = internal_code + 1  
                        new_result.flush()
                    else:
                        new_result.flush()
            except Exception as inst:
                logging.error("Error reading" + entry.find(name_space+"name").text)  
                logging.error(str(inst))  
    logging.info(" Process end" )



def convert_to_gate_gazetter(file, file_new):
    with open(file,'r') as dictionary:
        with open(file_new,'w') as gate_gazetter:
            firstline = dictionary.readline()
            column_names = [i.replace("\n","") for i in firstline.split('\t')]
            next(dictionary)
            for line in dictionary:
                data = line.split('\t')
                newline = data[1] + '\t' + column_names[0].replace("\n","") + '=' + data[0].replace("\n","")
                for a,b in zip(column_names[2:],data[2:]):
                    if b.strip()!='':
                        newline = newline + '\t' + a.replace("\n","") + '=' + b.replace("\n","")
                gate_gazetter.write(newline+'\n')
                gate_gazetter.flush()
