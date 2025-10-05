import 'package:card_wallet/l10n/app_localizations.dart';
import 'package:flutter/material.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({
    super.key, 
    required this.isDarkMode, 
    required this.onLanguageChanged,
    required this.onThemeChanged
  });

  final ValueChanged<bool> onThemeChanged;
  final ValueChanged<Locale> onLanguageChanged;
  final bool isDarkMode;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(AppLocalizations.of(context)!.settingsPageTitle)),
      body: ListView(
        children: [
          const SizedBox(height: 8),
          SwitchListTile(
            title: Text(AppLocalizations.of(context)!.darkModeTitle),
            subtitle: Text(AppLocalizations.of(context)!.darkModeSubtitle),
            value: isDarkMode,
            onChanged: (val) => onThemeChanged(val),
          ),
          ListTile(
            title: Text(AppLocalizations.of(context)!.languageTitle),
            subtitle: Text(Localizations.localeOf(context).languageCode == 'it'
                ? AppLocalizations.of(context)!.languageItalian
                : AppLocalizations.of(context)!.languageEnglish),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () => showDialog(
              context: context,
              builder: (context) => SimpleDialog(
                title: Text(AppLocalizations.of(context)!.selectLanguageDialogTitle),
                children: [
                  SimpleDialogOption(
                    child: Text(AppLocalizations.of(context)!.languageEnglish),
                    onPressed: () {
                      onLanguageChanged(const Locale('en'));
                      Navigator.pop(context);
                    },
                  ),
                  SimpleDialogOption(
                    child: Text(AppLocalizations.of(context)!.languageItalian),
                    onPressed: () {
                      onLanguageChanged(const Locale('it'));
                      Navigator.pop(context);
                    },
                  ),
                ],
              ),
            ),
          ),
          const Divider(),
          ListTile(
            title: Text(AppLocalizations.of(context)!.aboutTitle),
            trailing: const Icon(Icons.info_outline),
            onTap: () {
              showAboutDialog(
                context: context,
                applicationName: AppLocalizations.of(context)!.aboutAppName,
                applicationVersion: AppLocalizations.of(context)!.aboutVersion('1.0.0'),
                applicationLegalese: AppLocalizations.of(context)!.aboutCopyright,
              );
            },
          ),
          /*
          ListTile(
            title: const Text('Logout'),
            leading: const Icon(Icons.logout),
            textColor: Colors.red,
            iconColor: Colors.red,
            onTap: _logout,
          ),
          */
        ],
      ),
    );
  }
}
