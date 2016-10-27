import click
import xml.etree.ElementTree

@click.command()
@click.option('--android-sdk-version', 'attribute', flag_value='android-sdk-version', help='Retrieve Android SDK version.')
@click.option('--package-name', 'attribute', flag_value='package-name', help='Retrieve app\'s package name.')
@click.argument('manifest')
def tool(attribute, manifest):
    """Tool to read Android manifests."""
    manifest_node = xml.etree.ElementTree.parse(manifest).getroot()
    if 'package-name' == attribute:
        click.echo(manifest_node.get('package'))
    elif 'android-sdk-version' == attribute:
        click.echo(manifest_node.get('platformBuildVersionCode'))
