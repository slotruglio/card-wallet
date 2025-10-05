import 'package:card_wallet/pages/giftcards.dart';
import 'package:card_wallet/pages/settings.dart';
import 'package:card_wallet/pages/upload.dart';
import 'package:flutter/material.dart';
import 'package:card_wallet/l10n/app_localizations.dart';

class HomeWidget extends StatefulWidget {
  const HomeWidget({
    super.key, 
    required this.isDarkMode, 
    required this.onLanguageChanged,
    required this.onThemeChanged
  });

  final ValueChanged<bool> onThemeChanged;
  final ValueChanged<Locale> onLanguageChanged;
  final bool isDarkMode;

  @override
  State<HomeWidget> createState() => _HomeWidgetState();
}

class _HomeWidgetState extends State<HomeWidget> {
  int currentPageIndex = 0;

  @override
  Widget build(BuildContext context) {
    final ThemeData theme = Theme.of(context);
    return Scaffold(
      bottomNavigationBar: NavigationBar(
        onDestinationSelected: (int index) {
          setState(() {
            currentPageIndex = index;
          });
        },
        //indicatorColor: Colors.amber,
        selectedIndex: currentPageIndex,
        destinations: <Widget>[
          NavigationDestination(
            selectedIcon: Icon(Icons.home),
            icon: Icon(Icons.home_outlined),
            label: AppLocalizations.of(context)!.homeItem,
          ),
          NavigationDestination(
            icon: Icon(Icons.upload),
            label: AppLocalizations.of(context)!.addItem,
          ),
          NavigationDestination(
            icon: Icon(Icons.settings),
            label: AppLocalizations.of(context)!.settingsItem,
          ),
        ],
      ),
      body: <Widget>[
        /// Home page
        GiftCardListPage(),
        /// Upload page
        UploadPage(),

        /// Settings page
        SettingsPage(
          isDarkMode: widget.isDarkMode,
          onLanguageChanged: widget.onLanguageChanged,
          onThemeChanged: widget.onThemeChanged)
      ][currentPageIndex],
    );
  }
}