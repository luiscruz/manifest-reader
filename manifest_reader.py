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
        if not os.environ.get('ANDROID_HOME'):
            click.secho('Environment variable ANDROID_HOME is not defined.', err=True,fg='red')
            raise click.Abort
        aapk_output=check_output([os.environ['ANDROID_HOME']+"/build-tools/"+get_latest_sdk_version()+"/aapt", "dump","badging",input])
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

def get_latest_sdk_version():
    if os.environ.get('ANDROID_SDK'):
        return os.environ['ANDROID_SDK']
    build_tools_dir = os.environ['ANDROID_HOME']+"/build-tools/"
    return sorted(get_immediate_subdirectories(build_tools_dir))[-1]

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
