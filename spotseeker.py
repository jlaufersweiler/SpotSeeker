#-------------------------------------------------------------------------------
# Name:        SpotSeeker 2.1.1
# Purpose:  Collect spot files and assign them IDs
#
# Author:      Jonathan Laufersweiler
#
# Created:     06/25/2013
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()

import os,shutil,csv,glob

# *********** REPOSITORY LIST ************************

#Paths to source file repositories for various delivery services and clients
tela='//172.16.178.186/Catapult/Wisconsin/TelAmerica Media/' #location of telemerica files (SD & HD)
stldghd='//172.16.178.78/i/PreEncode/DG/DG-HD/' #Central Division HD DG files
stldgsd='//172.16.178.78/i/PreEncode/DG/DG-SD/' #Central Division SD DG files
edg='//172.25.112.59/encoded/PreEncode/DG_Spots/East_DG_Spots/' #East Division SD & HD DG files
widghd='//172.18.112.215/PreEncode/DG_VYVX/HD/720/' #WI DG HD Files
widgsd='//172.18.112.215/PreEncode/DG_VYVX/' #WI DG SD Files
mxrsd='//172.18.112.215/PreEncode/EXTREME_REACH/SD/' #Madison Extreme Reach SD files
mxrhd='//172.18.112.215/PreEncode/EXTREME_REACH/HD_1080/' #Madison Extreme Reach SD files
stlxr='//172.16.178.78/i/PreEncode/ExtremeReach/' #STL Extreme Reach (SD & HD)
exr='//172.25.112.59/encoded/PreEncode/ExtremeReach/' #East Division Extreme Reach (SD & HD)
smftp='//172.16.178.78/i/PreEncode/FROM_OUTSIDE_FTP/Superior Marketing/' #Superior Marketing FTP repository
smcat='//172.16.178.186/Catapult/Missouri/Superior Marketing Group/' #Superior Marketing Catapult backup
band='//172.16.178.186/Catapult/Corporate/The Band/' #The Band Catapult repository
slum='//172.18.112.215/PreEncode/FROM_OUTSIDE_FTP/Client/SLUMBERLAND/' #main Slumberland repository (SD)
cent='//172.16.178.186/Catapult/Centaur/' #Centaur Catapult directory
jvhd='//172.18.112.215/PreEncode/JAVELIN/HD/' #Javelin HD Repository
jvsd='//172.18.112.215/PreEncode/JAVELIN/SD/' #Javelin SD Repository
chmr='//172.16.178.186/Catapult/Corporate/Broadcaster Media/' #Broadcaster Marketing 'Corporate' Catapult directory SQ########
evnt='//172.16.178.186/Catapult/Missouri/Event Networks/' #Broadcaster Marketing 'PPV/VOD' Catapult Directory PPV### VOD#### etc
genie='//172.16.178.186/Catapult/Georgia/Decatur/SpotGenie/' #Spot Genie Catapult repository

#-----------------------------------
# The function below does most of the work here, comparing the client and tape information from the Eclipse data to the list of repositories above.
# There is a firewall doing deep packet inspection between here and many of these locations that makes directory listing a very slow operation,
# yet IO errors are returned instantly; thus the "Rumplestiltskin" method of try/except copy operations. Extensions are very explicitly used rather
# than wildcards or regex, as a false posative would cost the company money.
#-----------------------------------


def findspot(row): #function to seek, copy and rename files
    """Check each row for pattern matches, attempt to copy file, log to found.csv if successful, seek.csv if not."""
    retry=False
    if int(row.get('ULLENGTH'))>300: #EXCLUDE LONGFORM
        return retry

    elif row.get('SZTAPEINFO').upper() in ['VOD NON ENCODE','VOD NO ENCODE','Broadcaster.NET','NO ENCODE','NO ENCODE .NET','NO ENOCDE','DO NOT ENCODE','MAINSTREET','NO ENCOD E','NO ENCOD  E','DO NOT IMPORT','NON ENCODE','CNET - NO ENCODE','CNET NO ENCODE','DONE IN RENO']: #exclude things we don't encode
        return retry

    elif row.get('SZCOMPANY').upper().strip().startswith('LFLA') or row.get('SZSPOT').startswith('2S'): #exclude the LA office
        return retry

    elif 'TELAMERICA' in row.get('SZCOMPANY').upper():#TELAMERICA SPOTS
        print "Tela Hit"
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        try: #copy and rename file into the appropriate folder
            if ISCII.endswith('H'):
                shutil.copy2(''.join([tela,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                hit.writerow(record)
            elif ISCII.endswith('HD'):
                shutil.copy2(''.join([tela,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                hit.writerow(record)
            else:
                try:
                    shutil.copy2(''.join([tela,ISCII,'H.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
                except:
                    shutil.copy2(''.join([tela,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
        except:
            retry=True

    elif 'DG' in row.get('SZTAPEINFO').upper():#DG SPOTS
        print "DG Hit"
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        tinfo=row.get('SZTAPEINFO')
        try: #copy and rename file into the appropriate folder
            if KMA=='E' or 'East' in tinfo:
                if ISCII.endswith('H'):
                    shutil.copy2(''.join([edg,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
                else:
                    try:
                        shutil.copy2(''.join([edg,ISCII,'H.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except:
                        shutil.copy2(''.join([edg,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)

            elif 'WI' in tinfo: #Old MAD-SAN DG repository
                if ISCII.upper().endswith('H'): # If it ends in H, look for it in the HD repo
                    try:
                        shutil.copy2(''.join([widghd,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except: #if not in HD repo, look for SD
                        try:
                            shutil.copy2(''.join([widgsd,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                            hit.writerow(record)
                        except:
                            shutil.copy2(''.join([widgsd,ISCII,'.avi']),''.join(['./',KMA,'/',spotID,'.avi']))
                            hit.writerow(record)
                else: #isci doesn't end in H
                    try: #see if there is a version with an H suffix in the HD repo
                        shutil.copy2(''.join([widghd,ISCII,'h.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except: #otherwise grab from SD repo
                        try:
                            shutil.copy2(''.join([widgsd,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                            hit.writerow(record)
                        except:
                            shutil.copy2(''.join([widgsd,ISCII,'.avi']),''.join(['./',KMA,'/',spotID,'.avi']))
                            hit.writerow(record)
            #tape info doesn't specify Wisconsin, look in STL repo
            elif ISCII.upper().endswith('H'): # If it ends in H, look for it in the HD repo
                try:
                    shutil.copy2(''.join([stldghd,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
                except: #if not in HD repo, look for SD
                    try:
                        shutil.copy2(''.join([stldgsd,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except:
                        shutil.copy2(''.join([stldgsd,ISCII,'.avi']),''.join(['./',KMA,'/',spotID,'.avi']))
                        hit.writerow(record)
            else: #isci doesn't end in H
                try: #see if there is a version with an H suffix in the HD repo
                    shutil.copy2(''.join([stldghd,ISCII,'h.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
                except: #otherwise grab from SD repo
                    try:
                        shutil.copy2(''.join([stldgsd,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except:
                        shutil.copy2(''.join([stldgsd,ISCII,'.avi']),''.join(['./',KMA,'/',spotID,'.avi']))
                        hit.writerow(record)
        except:
                retry=True

    elif ('EXTR' or 'ER') in row.get('SZTAPEINFO').upper():#EXTREME REACH SPOTS
        print "Extreme Reach Hit"
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        tinfo=row.get('SZTAPEINFO')
        if KMA=='E' or 'East' in tinfo:
            if ISCII.endswith('H'):
                    shutil.copy2(''.join([exr,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                    hit.writerow(record)
            else:
                try:
                    shutil.copy2(''.join([exr,ISCII,'H.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                    hit.writerow(record)
                except:
                    shutil.copy2(''.join([exr,ISCII,'.avi']),''.join(['./',KMA,'/',spotID,'.avi']))
                    hit.writerow(record)

        elif 'MAD' in tinfo:
                if ISCII.upper().endswith('H'):
                    try:
                        shutil.copy2(''.join([mxrhd,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except:
                        retry=True
                else:
                    try:
                        shutil.copy2(''.join([mxrsd,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                        hit.writerow(record)
                    except:
                        retry=True
        else: #STL Extreme Reach repository
            if ISCII.upper().endswith('H'):
                    try:
                        shutil.copy2(''.join([stlxr,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except:
                        retry=True
            else:
                    try:
                        shutil.copy2(''.join([stlxr,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                        hit.writerow(record)
                    except:
                        retry=True

    elif 'THE BAND' in row.get('SZCOMPANY').upper(): # "The Band" spots
            print('The Band Hit')
            spotID=row.get('SZSPOT')
            ISCII=row.get('SZSPOTTITLE')
            print(spotID)
            print(ISCII)
            try:
                try:
                    shutil.copy2(''.join([band,ISCII,'.avi']),''.join(['./',KMA,'/',spotID,'.avi']))
                    hit.writerow(record)
                except:
                    shutil.copy2(''.join([band,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                    hit.writerow(record)
            except:
                retry=True

    elif ('Broadcaster' in row.get('SZCOMPANY').upper() or 'RETRANS' in row.get('SZCOMPANY').upper() or 'REGIONAL MARKETING' in row.get('SZCOMPANY').upper()): #Broadcaster Marketing spots
        print('Broadcaster Marketing hit')
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        if (ISCII.upper().startswith('SQ') or ISCII.upper().startswith('CC0')): # Corporate spots
            if ISCII.upper().startswith('SQ'):
                prefix=ISCII[0:8]
            elif ISCII.upper().startswith('CC0'):
                prefix=ISCII[0:5]
            else:
                prefix=ISCII
            if 'HD' in ISCII.upper():
                try:
                    try: #attempt to find .mpg version first, to avoid badly interlaced Broadcaster Marketing spots
                        shutil.copy2(glob.glob(''.join([chmr,prefix,'*.mpg']))[0].replace('\\','/'),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except: # if no .mpg, look for .mov
                        shutil.copy2(glob.glob(''.join([chmr,prefix,'*.mov']))[0].replace('\\','/'),''.join(['./',KMA,'/',spotID,'.mov']))
                        hit.writerow(record)
                except:
                    retry=True
            else:
                try:
                    try: #find spots without 'HD' in the Eclipse entry, bu where there is an HD version in the repository
                        try: #attempt to find .mpg version first, to avoid badly interlaced Broadcaster Marketing spots
                            shutil.copy2(glob.glob(''.join([chmr,prefix,'*HD.mpg']))[0].replace('\\','/'),''.join(['./',KMA,'/',spotID,'.mpg']))
                            hit.writerow(record)
                        except: # if no .mpg, look for .mov
                            shutil.copy2(glob.glob(''.join([chmr,prefix,'*HD.mov']))[0].replace('\\','/'),''.join(['./',KMA,'/',spotID,'.mov']))
                            hit.writerow(record)
                    except:
                        try:#There are HD movs that don have HD in the title. They will end up copied to the SD folder
                            try: #attempt to find .mpg version first, to avoid badly interlaced Broadcaster Marketing spots
                                shutil.copy2(glob.glob(''.join([chmr,prefix,'*.mpg']))[0].replace('\\','/'),''.join(['./',KMA,'/',spotID,'.mpg']))
                                hit.writerow(record)
                            except: # if no .mpg, look for .mov
                                shutil.copy2(glob.glob(''.join([chmr,prefix,'*.mov']))[0].replace('\\','/'),''.join(['./',KMA,'/',spotID,'.mov']))
                                hit.writerow(record)
                        except: #if neither mpg nor mov available, look for avi
                            shutil.copy2(glob.glob(''.join([chmr,prefix,'*.avi']))[0].replace('\\','/'),''.join(['./',KMA,'/',spotID,'.avi']))
                            hit.writerow(record)
                except:
                    retry=True
        else: #Event Marketing (VOD/PPV) spots
            try:
                try: # HD spots
                    try:
                        shutil.copy2(''.join([evnt,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                        hit.writerow(record)
                    except:
                        shutil.copy2(''.join([evnt,ISCII,'_HD.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                        hit.writerow(record)
                except:
                    try:
                        shutil.copy2(''.join([evnt,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except:
                        shutil.copy2(''.join([evnt,ISCII,'_HD.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
            except:
                    retry=True

    elif 'SUPERIOR MARKETING GROUP' in row.get('SZCOMPANY').upper():# SUPERIOR MARKETING GROUP SPOTS
        print "Superior Marketing Hit"
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        tinfo=row.get('SZTAPEINFO')
        if 'CAT' in tinfo: #catapult spots
            try:
                if ISCII.endswith('.'):
                    shutil.copy2(''.join([smcat,ISCII,'mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
                else:
                    shutil.copy2(''.join([smcat,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
            except:
                retry=True
        else: #FTP spots
            try:
                if ISCII.endswith('.'):
                    shutil.copy2(''.join([smftp,ISCII,'mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
                else:
                    shutil.copy2(''.join([smftp,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
            except:
                retry=True

    elif ('SLUMBERLAND' in row.get('SZCOMPANY').upper()) and (('MAD-SAN' in row.get('SZTAPEINFO')) or ('CAT' in row.get('SZTAPEINFO')))  :#SLUMBERLAND SPOTS -vanilla only, not production tagged
        print "Slumberland Hit"
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        if ISCII.upper().endswith('H'):
            try:
                shutil.copy2(''.join([slum,'HD/',ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                hit.writerow(record)
            except IOError:
                retry=True
        else:
            try:
                shutil.copy2(''.join([slum,'HD/',ISCII,'H.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                hit.writerow(record)
            except IOError:
                try:
                    shutil.copy2(''.join([slum,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                    hit.writerow(record)
                except IOError:
                    retry=True

    elif 'CENTAUR' in row.get('SZTAPEINFO').upper():#CENTAUR SPOTS
        print "Centaur Hit"
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        try: #copy and rename file into the appropriate folder, later make this find H's
            if ISCII.upper().endswith('H'):
                shutil.copy2(''.join([cent,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                hit.writerow(record)
            else:
                shutil.copy2(''.join([cent,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                hit.writerow(record)
        except:
            retry=True

    elif 'JAVELIN' in row.get('SZTAPEINFO').upper():#JAVELIN SPOTS
        print "Centaur Hit"
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        try: #copy and rename file into the appropriate folder, later make this find H's
            if ISCII.upper().endswith('H'):
                shutil.copy2(''.join([jvhd,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                hit.writerow(record)
            else:
                shutil.copy2(''.join([jvsd,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                hit.writerow(record)
        except:
            retry=True

    elif 'SG' in row.get('SZTAPEINFO').upper() or 'GENIE' in row.get('SZTAPEINFO').upper() :#SPOT GENIE
        print "Spot Genie Hit"
        spotID=row.get('SZSPOT')
        ISCII=row.get('SZSPOTTITLE')
        print(spotID)
        print(ISCII)
        try: #copy and rename file into the appropriate folder, later make this find H's
            if ISCII.endswith('H'):
                try:
                    shutil.copy2(''.join([genie,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                    hit.writerow(record)
                except:
                    shutil.copy2(''.join([genie,ISCII,'.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                    hit.writerow(record)
            else:
                try:
                    try:
                        shutil.copy2(''.join([genie,ISCII,'H.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except:
                        shutil.copy2(''.join([genie,ISCII,'H.mov']),''.join(['./',KMA,'/',spotID,'.mov']))
                        hit.writerow(record)
                except:
                    try:
                        shutil.copy2(''.join([genie,ISCII,'.mpg']),''.join(['./',KMA,'/',spotID,'.mpg']))
                        hit.writerow(record)
                    except:
                        shutil.copy2(''.join([genie,ISCII,'.avi']),''.join(['./',KMA,'/',spotID,'.avi']))
                        hit.writerow(record)

        except:
            retry=True
    else:
        print "No Hit"
        miss.writerow(row)
    return retry

#------------------------------------------------------------------------
#  Action starts
#-------------------------------------------------------------------------

#os.chdir('//172.16.178.78/i/PreEncode/SpotSeeker/')#set dir to working directory #UNCOMMENT THIS IF YOU WANT TO SPECIFY A DESTINATION DIRECTORY OTHER THAN THE DIRECTORY WHERE THE SCRIPT RESIDES.
#look for new copy reports
files=os.listdir('.')
if len(glob.glob('./*copyreport*.CSV'))==0: #csv's generated by Eclipse Web always have their extension capitalized
    print("No New Copy Report Found")
else: #if new reports found, begin processing
    for crfile in files:
        if (crfile.endswith('copyreport.CSV') or crfile.startswith('copyreport')): #find copy reports, the two options are for downloaded or emailed Eclipse Web files
            cr=crfile
            #set up files
            copyreport=open(cr,mode='r')
            rows=copyreport.readlines() #make list of rows
            copyreport.close()
            shutil.move(''.join(['./',cr]),''.join(['./OldReports/',cr])) #archive report
            ReportInfo=rows.pop(0) #Remove first row, store for analysis and output files
            if '.94' in ReportInfo:# Sets Great Lakes division based on IP address on first line of Copy Report
                KMA='GL'
            elif '.127' in ReportInfo:# Sets Midwest/West division based on IP address on first line of Copy Report
                KMA='MW'
                smclist=os.listdir(smcat) #list superior marketing Catapult directory, only used in MW
            elif '.22' in ReportInfo: # Sets Broadcaster marketing National Fulfillment Center based on IP address on first line of Copy Report
                KMA='NFC'
            else: # East's Eclipse is 172.21.176.31, but I'm leaving it like this in case they move it without telling me.
                KMA='E'
            current=open(''.join([KMA,'_WORKING.csv']),mode="w") #creates working copy, overwrites if exists
            current.writelines(rows)
            current.close()
            current=open(''.join([KMA,'_WORKING.csv']),mode="r") #switches to read-only
            found=open(''.join([KMA,'_FOUND.csv']),mode="w") #creates file for copied spots
            found.write(ReportInfo)
            found.close()
            found=open(''.join([KMA,'_FOUND.csv']),mode="a") #switches to append mode
            seek=open(''.join([KMA,'_SEEK.csv']),mode="w") #creates file for non-copied spots
            seek.write(ReportInfo)
            seek.close()
            seek=open(''.join([KMA,'_SEEK.csv']),mode="a") #switches to append mode
            #instantiate dictreader and dictwriters
            records=csv.DictReader(current,dialect='excel') #load data as list of key:value pairs
            hit=csv.DictWriter(found,fieldnames=["SZSALEPERSON","SZSALESPERSONNAME","SZSALESOFFICE","SZSALESOFFICENAME","SZORDER","ULDATE","SZHEADENDS","SZHEADENDDESC","SZNETWORKS","SZNETWORKDESC","SZSTATUS","UCENCODED","SZSPOT","SZSPOTTITLE","ULLENGTH","UCSPOTTYPE","SZCOMPANY","SZCUSTNUMBER","SZTAPEINFO","SZBKDSPOT","SZBKDTITLE","SZBKDLENGTH","SZBKDTAPE","SZCODE","SZDESCRIPTION"],restval='')
            hit.writeheader()
            miss=csv.DictWriter(seek,fieldnames=["SZSALEPERSON","SZSALESPERSONNAME","SZSALESOFFICE","SZSALESOFFICENAME","SZORDER","ULDATE","SZHEADENDS","SZHEADENDDESC","SZNETWORKS","SZNETWORKDESC","SZSTATUS","UCENCODED","SZSPOT","SZSPOTTITLE","ULLENGTH","UCSPOTTYPE","SZCOMPANY","SZCUSTNUMBER","SZTAPEINFO","SZBKDSPOT","SZBKDTITLE","SZBKDLENGTH","SZBKDTAPE","SZCODE","SZDESCRIPTION"],restval='')
            miss.writeheader()
            # start processing records
            for record in records:
                if KMA=='NFC': #NFC spot IDs require prepending of a capital M
                    ID=record.get('SZSPOT')
                    record.update({'SZSPOT':"".join(['M',ID])})
                retry=findspot(record) #initially parse record as-is
                if retry==True: #if findspot got a hit but couldn't successfully copy, try to fix the title and try again
                    titles=record.get('SZSPOTTITLE').split() #make list of all whitespace seperated title fragments
                    titles.append(record.get('SZSPOTTITLE').replace(' ','')) #all whole title with spaces stripped
                    for title in titles: #split 'isci-title' entries
                        if '-' in title:
                            fragments=title.split('-')
                            for fragment in fragments:#
                                titles.append(fragment)
                    fix=dict(record.items())
                while retry==True: #try to copy again with each of the fixed title possabilities generated above
                    fix.update({'SZSPOTTITLE':titles.pop(0).strip('()').replace('-','')})
                    retry=findspot(fix)
                    if (len(titles)==0 and retry==True):
                        print('Could not find:')
                        print(record.get('SZSPOTTITLE'))
                        #print(retry) #Uncomment this line to debug
                        miss.writerow(record)
                        retry=False
            current.close()
            found.close()
            seek.close()













