# -*- coding: utf-8 -*-
# Date    : 2025-11-06 10:20:26
# Author  : Marcio Yamashita (marcio.yamashita@fugro.com)
# Version : 0.1
# Goal    : Request erd

from fugropylib import Erddap
import numpy as np
import pandas as pd
import datetime as dtm
from zoneinfo import ZoneInfo
import smtplib
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.text import MIMEText
# We can just use the 80% success rate for the monthly return calculation 
# for the PASS/FAIL criteria on these emails. 
# Then, the other two options would be FAIL – MISSING or FAIL – INCOMPLETE.

#Setup Station
buoySN  = 'WS007'
aqd_cutoff = 42
sig_cutoff = 702
battery_threshold = 12
################
utc_hour = dtm.datetime.now(dtm.timezone.utc).replace(
    minute=0, second=0, microsecond=0)
utc_hour = dtm.datetime.now(dtm.timezone.utc).replace(day=10, hour=12,
    minute=0, second=0, microsecond=0)
# Convert to Central Time (automatically handles DST)
central_time = utc_hour.astimezone(ZoneInfo("America/Chicago"))
time_end = utc_hour.replace(tzinfo=None)
time_ini = time_end - dtm.timedelta(hours=167)

expected_wave = pd.date_range(time_ini, time_end, freq='30min')
expected_wind = pd.date_range(time_ini, time_end, freq='30min')
expected_met = pd.date_range(time_ini, time_end, freq='30min')
expected_bat = pd.date_range(time_ini, time_end, freq='30min')
expected_aqd = pd.date_range(time_ini, time_end, freq='20min')
expected_adcp = pd.date_range(time_ini, time_end, freq='20min')


e = Erddap(server="http://10.1.1.17:8080/erddap",
           dataset_id='geosOceanorWave',
           constraints={'id=':buoySN, 'time>=': time_ini, 'time<=': time_end})
    #Marcus ordered this variables
e.variables = ['time', 'Hm0', 'Hmax', 'Mdir', 'Tp']
try:
    df_wave = e.to_pandas()
except:
    df_wave=pd.DataFrame(columns=['Hm0', 'Hmax', 'Mdir', 'Tp'])

df_wave_qc = df_wave
df_wave_qc = df_wave_qc[(df_wave_qc['Hm0'] > 0) & (df_wave_qc['Hm0'] < 12.5)]
df_wave_qc = df_wave_qc[(df_wave_qc['Mdir'] > 0) & (df_wave_qc['Mdir'] < 360)]
df_wave_qc = df_wave_qc[(df_wave_qc['Tp'] > 2) & (df_wave_qc['Tp'] < 28)]

QC_WAVE = df_wave_qc['Hm0'].count().sum() / len(expected_wave)
# QC_WAVE=0 #FORCED TO TEST FLAG

if QC_WAVE >= 0.8:
    wave_data = f'<span style="color:green;">PASS.</span>'
elif ((QC_WAVE > 0) & (QC_WAVE < 0.8)):
    wave_data = (f'<span style="color:red;">FAIL - INCOMPLETE.</span>'
                 f'<br><b>Wave data percentage:</b> {QC_WAVE:.2%}<hr>')
else:
    wave_data = f'<span style="color:red;">FAIL - MISSING.</span>'

###############################
e.dataset_id = "geosOceanorWind"
e.variables = ['time', 'altitude', 'WindDirection', 'WindGust', 'WindSpeed']
try:
    df_wind = e.to_pandas()
except:
    df_wind = pd.DataFrame(columns=['altitude', 'WindDirection', 'WindGust', 'WindSpeed'])
    df_wind.loc['altitude'] = 3.50
df_wind_qc = df_wind
df_wind_qc = df_wind_qc[(df_wind_qc['WindSpeed'] > 0) & (df_wind_qc['WindSpeed'] < 25)]
df_wind_qc = df_wind_qc[(df_wind_qc['WindDirection'] > 0) & (df_wind_qc['WindDirection'] < 360)]

df_wind_qc = df_wind_qc.pivot(columns='altitude')
df_wind_qc = df_wind_qc.reindex(expected_wind)

QC_WIND = df_wind_qc['WindSpeed'].count().sum() / (df_wind_qc['WindSpeed'].shape[1]*len(expected_wind))
if QC_WIND >= 0.8:
    wind_data = f'<span style="color:green;">PASS.</span>'
elif ((QC_WIND > 0) & (QC_WIND < 0.8)):
    wind_data = (f'<span style="color:red;">FAIL - INCOMPLETE.</span>'
                 f'<br><b>Wind data percentage:</b> {QC_WIND:.2%}<hr>')
else:
    wind_data = f'<span style="color:red;">FAIL - MISSING.</span>'

###############################
e.dataset_id = "geosOceanorMet"
e.variables = ['time', 'AirPressure', 'AirTemperature', 'AirHumidity']
try:
    df_met = e.to_pandas()
except:
    df_met = pd.DataFrame(columns=['AirPressure', 'AirTemperature', 'AirHumidity'])


df_pressure_qc = df_met['AirPressure'] * 0.01
df_pressure_qc = df_pressure_qc[(df_pressure_qc > 800) & (df_pressure_qc < 1100)]
df_airtemp_qc = df_met['AirTemperature'] - 273.15
df_airtemp_qc = df_airtemp_qc[(df_airtemp_qc > -10) & (df_airtemp_qc < 35)]
df_airhumi_qc = df_met['AirHumidity']
df_airhumi_qc = df_airhumi_qc[(df_airhumi_qc > 5) & (df_airhumi_qc < 100)]

QC_Press = df_pressure_qc.count().sum() / len(expected_met)
QC_Airtemp = df_airtemp_qc.count().sum() / len(expected_met)
QC_Airhumi = df_airhumi_qc.count().sum() / len(expected_met)

#QC_Airtemp=0 #FORCED TO TEST FLAG
QC_MET = np.mean([QC_Press, QC_Airtemp, QC_Airhumi])

if QC_MET >= 0.8:
    met_data = f'<span style="color:green;">PASS.</span>'
elif ((QC_MET > 0) & (QC_MET < 0.8)):
    met_data = (f'<span style="color:red;">FAIL - INCOMPLETE.</span>'
                f'<br><b>Air Pressure data percentage:</b> {QC_Press:.2%}'
                f'<br><b>Air Temperature data percentage:</b> {QC_Airtemp:.2%}'
                f'<br><b>Air Humidity data percentage:</b> {QC_Airhumi:.2%}<hr>') 
else:
    met_data = f'<span style="color:red;">FAIL - MISSING.</span>'

###############################
e.dataset_id = "geosOceanorAquadopp"
e.variables = ['time', 'depth', 'AqSpd', 'AqDir']
try:
    df_aqd = e.to_pandas()
except:
    df_aqd = pd.DataFrame(columns=['depth', 'AqSpd', 'AqDir'])
    df_aqd.loc['depth'] = 1

df_aqd_qc = df_aqd[df_aqd.depth < aqd_cutoff]
df_aqd_qc = df_aqd_qc[(df_aqd_qc['AqSpd'] > 0) & (df_aqd_qc['AqSpd'] < 2.5)]
df_aqd_qc = df_aqd_qc[(df_aqd_qc['AqDir'] > 0) & (df_aqd_qc['AqDir'] < 360)]

df_aqd_qc = df_aqd_qc.pivot(columns='depth')
df_aqd_qc = df_aqd_qc.reindex(expected_aqd)

QC_AQD = df_aqd_qc['AqSpd'].count().sum() / (df_aqd_qc['AqSpd'].shape[1]*len(expected_aqd))
if QC_AQD >= 0.8:
    aquadopp_data = f'<span style="color:green;">PASS.</span>'
elif ((QC_AQD > 0) & (QC_AQD < 0.8)):
    aquadopp_data = (f'<span style="color:red;">FAIL - INCOMPLETE.</span>'
                     f'<br><b>Aquadopp current data percentage:</b> {QC_AQD:.2%}<hr>')
else:
    aquadopp_data = f'<span style="color:red;">FAIL - MISSING.</span>'

###############################
e.dataset_id = "geosOceanorADCP"
e.variables = ['time', 'depth', 'CurrSpd', 'CurrDir']
try:
    df_adcp = e.to_pandas()
except:
    df_adcp = pd.DataFrame(columns=['depth', 'CurrSpd', 'CurrDir'])
    df_adcp.loc['depth'] = 1

# QC part before pivot
df_adcp_qc = df_adcp[df_adcp.depth < sig_cutoff]
df_adcp_qc = df_adcp_qc[(df_adcp_qc['CurrSpd'] > 0) & (df_adcp_qc['CurrSpd'] < 2.5)]
df_adcp_qc = df_adcp_qc[(df_adcp_qc['CurrDir'] > 0) & (df_adcp_qc['CurrDir'] < 360)]

df_adcp_qc = df_adcp_qc.pivot(columns='depth')

df_adcp_qc = df_adcp_qc.reindex(expected_aqd)
QC_ADCP = df_adcp_qc['CurrSpd'].count().sum() / (df_adcp_qc['CurrSpd'].shape[1]*len(expected_adcp))
if QC_ADCP >= 0.8:
    signature_data = f'<span style="color:green;">PASS.</span>'
elif ((QC_ADCP > 0) & (QC_ADCP < 0.8)):
    signature_data = (f'<span style="color:red;">FAIL - INCOMPLETE.</span>'
                      f'<br><b>Signature 55 current data percentage:</b> {QC_ADCP:.2%}<hr>')
else:
    signature_data = f'<span style="color:red;">FAIL - MISSING.</span>'


###############################
e.dataset_id = "geosOceanorBuoyData"
e.variables = ['time', 'LeadBatteryVoltage']
try:
    df_battery = e.to_pandas()
except:
    df_battery = pd.DataFrame(columns=['LeadBatteryVoltage'])
    df_battery.loc['LeadBatteryVoltage'] = -1

df_battery_qc = df_battery['LeadBatteryVoltage'] >= battery_threshold
QC_BATT = df_battery_qc.sum() / len(expected_bat)

if df_battery.iloc[0, -1] >= battery_threshold:
    battery_data = f'<span style="color:green;">PASS.</span>'
else:
    battery_data = f'<span style="color:red;">FAIL.</span>'

# send email ###################################################################
# html body is for client
html_body = f"""\
<html>
  <body>
    <p><b>This is an automated message. Please do not reply.</b><br>
    Please find below the weekly buoy status from {buoySN} between
    {time_ini:%Y-%b-%d %H:%M} UTC and {time_end:%Y-%b-%d %H:%M} UTC.</p>

    <p><b>Wind data:</b> {wind_data}</p>
    <p><b>Wave data:</b> {wave_data}</p>
    <p><b>Meteorological data:</b> {met_data}</p>
    <p><b>Aquadopp current data:</b> {aquadopp_data}</p>
    <p><b>Signature 55 current data:</b> {signature_data}</p>
    <p><b>Battery data LeadBatteryVoltage:</b> {battery_data}</p>

    <p>Please do not hesitate to contact us should you have any questions or concerns 
    (mailto:j.fredrickson@fugro.com</a>).</p>
  </body>
</html>
"""

# html body_PM is for PM INTERNAL
html_body_PM = f"""\
<html>
  <body>
    <p><b>This email is an automated message and is intended for
        <span style="color:red;">internal use only</span>.<br></b>
        Please find below the weekly buoy status from {buoySN} between
        {time_ini:%Y-%b-%d %H:%M} UTC and {time_end:%Y-%b-%d %H:%M} UTC.</p>

    <p><b>Wind data:</b> {wind_data}</p>
    <p><b>Wind data percentage:</b> {QC_WIND:.2%}</p><hr>

    <p><b>Wave data:</b> {wave_data}</p>
    <p><b>Wave data percentage:</b> {QC_WAVE:.2%}</p><hr>

    <p><b>Meteorological data:</b> {met_data}</p>
    <p><b>Air Pressure data percentage:</b> {QC_Press:.2%}</p>
    <p><b>Air Temperature data percentage:</b> {QC_Airtemp:.2%}</p>
    <p><b>Air Humidity data percentage:</b> {QC_Airhumi:.2%}</p><hr>

    <p><b>Aquadopp current data:</b> {aquadopp_data}</p>
    <p><b>Aquadopp current data percentage:</b> {QC_AQD:.2%}</p>
    <p>Aquadopp cutoff: {aqd_cutoff} m.</p><hr>

    <p><b>Signature 55 current data:</b> {signature_data}</p>
    <p><b>Signature 55 current data percentage:</b> {QC_ADCP:.2%}</p>
    <p>Signature cutoff: {sig_cutoff} m.</p><hr>

    <p><b>Battery data LeadBatteryVoltage:</b> {battery_data}</p>
    <p>Battery time: { df_battery.index[-1]} UTC, value: {df_battery.iloc[0,-1]} V</p>
    <p>Battery data percentage equal or greater than <b>{battery_threshold} V:</b> {QC_BATT:.2%}</p><hr>

    <p>Please do not hesitate to contact us should you have any questions or concerns 
    (mailto:j.fredrickson@fugro.com</a>).</p>
  </body>
</html>
"""

FROM = "oceanforecast@fugro.com"
HOST = "USHOUSSMTP01.ad.fugro.com"
#TO = ['JJ_Xia@contractor.murphyoilcorp.com', 'j.fredrickson@fugro.com'] #
TO = ['j.fredrickson@fugro.com'] #
SUBJECT = [f'MURPHY BUOY DATA STATUS {central_time:%Y-%b-%d}']
msg = MIMEMultipart('related')
msg["From"] = FROM
msg["To"] = ', '.join(TO)
msg["Subject"] = ', '.join(SUBJECT)
msg['Date'] = formatdate(localtime=True)
msg.preamble = 'This is a multi-part message in MIME format.'

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)
msgTextHtml = MIMEText(html_body, 'html')
msgAlternative.attach(msgTextHtml)

server = smtplib.SMTP(HOST)
#server.set_debuglevel(True)
try: 
    server.login('sa-usa-metocean-data','VSL1Y&npw1!d')
    server.sendmail(FROM, TO, msg.as_string())
    server.close()
except:
    with open('log.txt', 'a') as f:
        f.write(f'Unable to send email with {html_body_PM}.')


# EMAIL TO PM ##################################################################
TO = ['j.fredrickson@fugro.com']
#TO = ['marcio.yamashita@fugro.com']

SUBJECT = [f'MURPHY BUOY DATA STATUS {central_time:%Y-%b-%d} - INTERNAL']
msg = MIMEMultipart('related')
msg["From"] = FROM
msg["To"] = ', '.join(TO)
msg["Subject"] = ', '.join(SUBJECT)
msg['Date'] = formatdate(localtime=True)
msg.preamble = 'This is a multi-part message in MIME format.'

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)
msgTextHtml = MIMEText(html_body_PM, 'html')
msgAlternative.attach(msgTextHtml)

""" # attach a file
part = MIMEBase('application', "octet-stream")
part.set_payload( open(out_file_name,"r").read() )
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(out_file_name))
msg.attach(part) """
 
server = smtplib.SMTP(HOST)
#server.set_debuglevel(True)
try: 
    server.login('sa-usa-metocean-data','VSL1Y&npw1!d')
    server.sendmail(FROM, TO, msg.as_string())
    server.close()
except:
    with open('log.txt', 'a') as f:
        f.write(f'Unable to send email with {html_body_PM}.')


