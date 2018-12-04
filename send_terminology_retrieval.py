import sys
import argparse
import ConfigParser
import urllib, urllib2
import os
import logging
import xml.etree.ElementTree as ET

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
  "BH": "Behavioral",
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
  "IC": "IMPLATATION_CLASSIFICATION_DOMAIN",
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
  "VS": "VITAL_SIGNS_DOMAIN"
}


def Main(parameters):
    output=parameters['output']
    outputDict=parameters['outputDict']
    if not os.path.exists(output):
        os.makedirs(output)
    
    send_terminology_cdi_url = parameters['send_terminology_cdi_url']
    etox_send_codelists = parameters['etox_send_codelists']
    etox_send_codelist_terms = parameters['etox_send_codelist_terms']
    etox_send_codelist_synonyms = parameters['etox_send_codelist_synonyms']
    etox_output = parameters['etox_output']
    
    generate_send_etox_corpus(etox_send_codelists, etox_send_codelist_terms, etox_send_codelist_synonyms, etox_output)
    outputFileSEND = output+"/send_terminology_search.xml"
    
    download_send_cdis_terminology(send_terminology_cdi_url, outputFileSEND)
    outputFileFilter = outputDict
    generate_send_cdis_corpus(outputFileSEND, outputFileFilter)
    
def ReadParameters(args):
    if(args.p!=None):
        Config = ConfigParser.ConfigParser()
        Config.read(args.p)
        parameters['output']=Config.get('MAIN', 'output')
        parameters['outputDict']=Config.get('MAIN', 'outputDict')
        
        parameters['send_terminology_cdi_url']=Config.get('MAIN', 'send_terminology_cdi_url')
        
        parameters['etox_send_codelists']=Config.get('MAIN', 'etox_send_codelists')
        parameters['etox_send_codelist_terms']=Config.get('MAIN', 'etox_send_codelist_terms')
        parameters['etox_send_codelist_synonyms']=Config.get('MAIN', 'etox_send_codelist_synonyms')
        parameters['etox_output']=Config.get('MAIN', 'etox_output')
    else:
        logging.error("Please send the correct parameters config.properties --help ")
        sys.exit(1)
    return parameters   


def generate_send_etox_corpus(etox_send_codelists, etox_send_codelist_terms, etox_send_codelist_synonyms, outputfile):
    logging.info("generate_etox_corpus  " )
    with open(etox_send_codelists,'r') as code_list: 
        with open(etox_send_codelist_terms,'r') as terms:
            with open(etox_send_codelist_synonyms,'r') as synonyms:
                with open(outputfile,'w') as new_result: 
                    new_result.write('keyword\tcodelist_acronym\tcodelist_id\tterm_id\ttype\tterm_name\tsynonym_type\tsource\n')
                    new_result.flush()
                    for line_codelist in code_list:
                        data_codelist = line_codelist.split('\t')
                        if(data_codelist[0]!='CODELIST_ID'):
                            terms.seek(0)
                            for line_term in terms:
                                data_term = line_term.split('\t')
                                if(data_codelist[0]==data_term[0] and data_codelist[0]!='CODELIST_ID'):
                                    new_result.write(data_term[2] + '\t' + data_codelist[2] + '\t' + data_term[0] + '\t' + data_term[1] + '\tprimary' +'\t\t\t\n' )
                                    new_result.flush()
                                    synonyms.seek(0)
                                    for line_syn in synonyms:
                                        data_syn = line_syn.split('\t')
                                        if(data_syn[1]==data_term[1] and data_syn[0]!='CODELIST_ID'):
                                            new_result.write(data_syn[2] + '\t' + data_codelist[2] + '\t' + data_term[0] + '\t' + data_term[1] + '\tsynonym' + '\t' + data_term[2] + '\t' + data_syn[3] + '\t' + data_syn[4])
                                    new_result.flush()        
                            
    logging.info(" Process end" )

def download_send_cdis_terminology(send_terminology_url, outputFile):
    logging.info("Downloading SEND Terminology from : " + send_terminology_url )
    url = send_terminology_url
    params = urllib.urlencode({})
    request = urllib2.Request(url, params)
    response = urllib2.urlopen(request)
    response_cyps = response.read()
    with open(outputFile,'w') as result: 
        result.write(response_cyps)
        result.flush()
    logging.info("Download End ")  

def generate_send_cdis_corpus(unputUniprotFile, outputFile):
    logging.info("generate_send_cdis_corpus " )
    name_space = "{http://www.cdisc.org/ns/odm/v1.3}"
    nciodm_name_space="{http://ncicb.nci.nih.gov/xml/odm/EVS/CDISC}"
    docXml = ET.parse(unputUniprotFile)
    root = docXml.getroot()
    with open(outputFile,'w') as new_result: 
        new_result.write('keyword\toid_code\toid_id\tkeyword_type\t\n')
        study_xml = root.find(name_space+"Study")
        metadataversion_xml = study_xml.find(name_space+"MetaDataVersion")
        for entry in metadataversion_xml.findall(name_space+"CodeList"):
            try:
                oid=entry.attrib.get("OID")
                oid_i = oid.rfind('.')
                oid=oid[oid_i+1:]
                for item in entry.findall(name_space+"EnumeratedItem"):
                    code = item.attrib.get("CodedValue")
                    if (send_domain.get(code) is not None):
                        code = send_domain.get(code)
                    nciodm_ExtCodeID = item.attrib.get(nciodm_name_space+"ExtCodeID")
                    for syn in item.findall(nciodm_name_space+"CDISCSynonym"):
                        new_result.write(syn.text+'\t'+ code.replace(" ","_") +'\t'+ nciodm_ExtCodeID +'\t'+ 'synonym'+'\n')
                    nciodm_PreferredTerm=item.find(nciodm_name_space+"PreferredTerm")   
                    new_result.write(nciodm_PreferredTerm.text+'\t'+ code.replace(" ","_") +'\t'+ nciodm_ExtCodeID +'\t'+ 'preferred_term'+'\n')
                    new_result.flush()
            except Exception as inst:
                print "Error reading " + entry.find(name_space+"name").text
                print str(inst)
    logging.info(" Process end" )




