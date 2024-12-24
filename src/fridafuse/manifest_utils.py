from __future__ import annotations

from pathlib import Path

from defusedxml.ElementTree import parse

from fridafuse import constants, utils


def get_root_manifest(manifest_file: Path):
    if not manifest_file.is_file():
        return None

    tree = parse(manifest_file)

    return tree.getroot()


def get_main_activity(manifest_file: Path):
    root = get_root_manifest(manifest_file)

    if root is not None:
        for activity in root.findall('.//activity', namespaces=constants.MANIFEST_NAMESPACE):
            for intent_filter in activity.findall('.//intent-filter', namespaces=constants.MANIFEST_NAMESPACE):
                has_main_action = any(
                    action.get(f'{{{constants.MANIFEST_NAMESPACE["android"]}}}name') == 'android.intent.action.MAIN'
                    for action in intent_filter.findall('action', namespaces=constants.MANIFEST_NAMESPACE)
                )
                has_launcher_category = any(
                    category.get(f'{{{constants.MANIFEST_NAMESPACE["android"]}}}name')
                    == 'android.intent.category.LAUNCHER'
                    for category in intent_filter.findall('category', namespaces=constants.MANIFEST_NAMESPACE)
                )

                if has_main_action and has_launcher_category:
                    return activity.get(f'{{{constants.MANIFEST_NAMESPACE["android"]}}}name')

    return None


def get_main_activity_path(manifest_file: Path):
    main_activity = get_main_activity(manifest_file)

    if not main_activity:
        return None

    smali_file = Path(f"{main_activity.replace('.', '/')}.smali")
    smali_dirs = [d for d in manifest_file.parent.iterdir() if d.is_dir() and d.name.startswith('smali')]

    return utils.find_file(smali_file, smali_dirs)


def is_extract_native_libs_enabled(manifest_file: Path):
    root = get_root_manifest(manifest_file)

    if root is not None:
        application_element = root.find('application', namespaces=constants.MANIFEST_NAMESPACE)
        if application_element is not None:
            extract_native_libs = application_element.get(
                f'{{{constants.MANIFEST_NAMESPACE["android"]}}}extractNativeLibs'
            )

            return extract_native_libs != 'false'

    return None
