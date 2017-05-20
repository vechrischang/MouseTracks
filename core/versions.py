VERSION_HISTORY = [
    '2.0',
    '2.0.1',
    '2.0.1b',
    '2.0.2',
    '2.0.3',
    '2.0.4',
    '2.0.5',
    '2.0.5b',
    '2.0.6'
]
VERSION = VERSION_HISTORY[-1]

def _get_id(id):
    """Read the ID for upgrading versions.
    If no ID exists, such as if the version may not be finished,
    it'll default to the first ID and not upgrade.
    """
    try:
        return VERSION_HISTORY.index(str(id))
    except ValueError:
        return 0

def upgrade_version(data):
    """Files from an older version will be run through this function.

    History:
    2.0: Base script
    2.0.1: Add acceleration tracking
    2.0.1b: Rename acceleration to speed, change tracking method
    2.0.2: Experimenting with combined speed and position tracks
    2.0.3: Separate click maps, record both keys pressed and how long
    2.0.4: Save creation date and rename modified date
    2.0.5: Group maps and add extras for experimenting on
    2.0.5b: Separate tick counts for different maps
    2.0.6: Remove speed and combined maps as they don't look very interesting
    """

    #Make sure version is in history, otherwise set to lowest version
    current_version_id = _get_id(data['Version'])
    
    if current_version_id < _get_id('2.0.1'):
        data['Acceleration'] = {}
    if current_version_id < _get_id('2.0.1b'):
        del data['Acceleration']
        data['Speed'] = {}
    if current_version_id < _get_id('2.0.2'):
        data['Combined'] = {}
    if current_version_id < _get_id('2.0.3'):
        data['Clicks'] = {}
        data['Keys'] = {'Pressed': {}, 'Held': {}}
        data['Ticks'] = {'Current': data['Count'],
                         'Total': data['Ticks'],
                         'Recorded': data['Count']}
        del data['Count']
    if current_version_id < _get_id('2.0.4'):
        data['Time'] = {'Created': data['LastSave'],
                        'Modified': data['LastSave']}
        del data['LastSave']
    if current_version_id < _get_id('2.0.5'):
        data['Maps'] = {'Tracks': data['Tracks'], 'Clicks': data['Clicks'],
                        'Speed': data['Speed'], 'Combined': data['Combined'],
                        'Temp1': {}, 'Temp2': {}, 'Temp3': {}, 'Temp4': {},
                        'Temp5': {}, 'Temp6': {}, 'Temp7': {}, 'Temp8': {}}
        del data['Tracks']
        del data['Clicks']
        del data['Speed']
        del data['Combined']
    if current_version_id < _get_id('2.0.5b'):
        data['Ticks']['Current'] = {'Tracks': data['Ticks']['Current'],
                                    'Speed': data['Ticks']['Current']}
    if current_version_id < _get_id('2.0.6'):
        del data['Maps']['Speed']
        del data['Maps']['Combined']
        del data['Ticks']['Current']['Speed']
    
    data['Version'] = VERSION
    return data
