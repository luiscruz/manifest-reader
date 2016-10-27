import click
import xml.etree.ElementTree as ET
from subprocess import check_output
import os

@click.command()
@click.option('--android-sdk-version', 'attribute', flag_value='android-sdk-version', help='Retrieve Android SDK version.')
@click.option('--package-name', 'attribute', flag_value='package-name', help='Retrieve app\'s package name.')
@click.option('--version-name', 'attribute', flag_value='version-name', help='Retrieve app\'s version name.')
@click.option('--xml/--apk', default=True, help='specify input type')
@click.argument('input')
def tool(attribute, xml, input):
    """Tool to read Android manifests. Works with APK files."""
    if xml:
        manifest_node = ET.parse(input).getroot()
        if 'package-name' == attribute:
            click.echo(manifest_node.get('package'))
        elif 'android-sdk-version' == attribute:
            click.echo(manifest_node.get('platformBuildVersionCode'))
        elif 'version-name' == attribute:
            click.echo(manifest_node.get('android:versionName'))
    else:
        aapk_output=check_output([os.environ['ANDROID_HOME']+"/build-tools/23.0.1/aapt", "dump","badging",input])
        if 'package-name' == attribute:
            package_line = parse_aapk(aapk_output, 'package')
            click.echo(parse_aapk_attribute_line(package_line, 'name'))
        elif 'android-sdk-version' == attribute:
            click.echo(parse_aapk(aapk_output, 'targetSdkVersion').replace("'",""))
        elif 'version-name' == attribute:
            package_line = parse_aapk(aapk_output, 'package')
            click.echo(parse_aapk_attribute_line(package_line, 'versionName'))
        
def parse_aapk(aapk_output, key):
    for line in aapk_output.split(os.linesep):
        line_key,line_value = line.split(':')
        if line_key==key:
            return line_value
        
def parse_aapk_attribute_line(aapk_line, attribute):
    pairs=aapk_line.split(" ")
    for pair in pairs:
        splited = pair.split('=')
        if len(splited) == 2:
            this_attribute,this_value=splited
            if this_attribute == attribute:
                return this_value.replace("'","")