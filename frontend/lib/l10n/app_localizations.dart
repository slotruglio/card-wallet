import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_it.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
    : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
        delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('it'),
  ];

  /// The conventional newborn programmer greeting
  ///
  /// In en, this message translates to:
  /// **'Hello World!'**
  String get helloWorld;

  /// Home navigation item
  ///
  /// In en, this message translates to:
  /// **'Home'**
  String get homeItem;

  /// Add navigation item
  ///
  /// In en, this message translates to:
  /// **'Add'**
  String get addItem;

  /// Settings navigation item
  ///
  /// In en, this message translates to:
  /// **'Setting'**
  String get settingsItem;

  /// Text for no more gift card in home
  ///
  /// In en, this message translates to:
  /// **'🎉 No more gift cards'**
  String get noMoreGiftCardText;

  /// Amount text with variable
  ///
  /// In en, this message translates to:
  /// **'Amount: {amount}'**
  String amountText(String amount);

  /// Expiration text with variable
  ///
  /// In en, this message translates to:
  /// **'Expires on {expirationDate}'**
  String expirationDateText(String expirationDate);

  /// gift card page title
  ///
  /// In en, this message translates to:
  /// **'Gift Cards'**
  String get giftCardPageTitle;

  /// Text for successfull upload
  ///
  /// In en, this message translates to:
  /// **'Gift card uploaded successfully!'**
  String get giftCardUploadSuccessText;

  /// Upload gift card message
  ///
  /// In en, this message translates to:
  /// **'Upload Gift Card'**
  String get giftCardUploadText;

  /// Supplier text
  ///
  /// In en, this message translates to:
  /// **'Supplier'**
  String get supplierText;

  /// Text for supplier validation
  ///
  /// In en, this message translates to:
  /// **'Enter supplier name'**
  String get supplierValidationText;

  /// Text for amount
  ///
  /// In en, this message translates to:
  /// **'Amount'**
  String get amountFormText;

  /// Text for amount validation
  ///
  /// In en, this message translates to:
  /// **'Enter amount'**
  String get amountValidationText;

  /// Text for amount wrong number
  ///
  /// In en, this message translates to:
  /// **'Enter a valid number'**
  String get amountWrongText;

  /// Text for expiration date form
  ///
  /// In en, this message translates to:
  /// **'Expiration Date'**
  String get expirationDateFormText;

  /// tooltip for expiration date
  ///
  /// In en, this message translates to:
  /// **'Tap to select date'**
  String get expirationDateFormTooltip;

  /// text for select file form
  ///
  /// In en, this message translates to:
  /// **'Select File'**
  String get fileFormText;

  /// text for gift card uploading
  ///
  /// In en, this message translates to:
  /// **'Uploading...'**
  String get uploadingText;

  /// text for upload button
  ///
  /// In en, this message translates to:
  /// **'Upload Gift Card'**
  String get uploadGiftCardButtonText;

  /// Title of the settings page
  ///
  /// In en, this message translates to:
  /// **'Settings'**
  String get settingsPageTitle;

  /// Title for dark mode toggle
  ///
  /// In en, this message translates to:
  /// **'Dark Mode'**
  String get darkModeTitle;

  /// Subtitle for dark mode toggle
  ///
  /// In en, this message translates to:
  /// **'Use dark theme throughout the app'**
  String get darkModeSubtitle;

  /// Title for notifications toggle
  ///
  /// In en, this message translates to:
  /// **'Notifications'**
  String get notificationsTitle;

  /// Subtitle for notifications toggle
  ///
  /// In en, this message translates to:
  /// **'Receive push notifications'**
  String get notificationsSubtitle;

  /// Title for language selection option
  ///
  /// In en, this message translates to:
  /// **'Language'**
  String get languageTitle;

  /// Dialog title for selecting language
  ///
  /// In en, this message translates to:
  /// **'Select Language'**
  String get selectLanguageDialogTitle;

  /// Option for English language
  ///
  /// In en, this message translates to:
  /// **'English'**
  String get languageEnglish;

  /// Option for Italian language
  ///
  /// In en, this message translates to:
  /// **'Italiano'**
  String get languageItalian;

  /// Option for Spanish language
  ///
  /// In en, this message translates to:
  /// **'Español'**
  String get languageSpanish;

  /// Title for about section
  ///
  /// In en, this message translates to:
  /// **'About'**
  String get aboutTitle;

  /// Name of the app displayed in About dialog
  ///
  /// In en, this message translates to:
  /// **'GiftCard Manager'**
  String get aboutAppName;

  /// Version displayed in About dialog
  ///
  /// In en, this message translates to:
  /// **'Version {version}'**
  String aboutVersion(String version);

  /// Copyright text in About dialog
  ///
  /// In en, this message translates to:
  /// **'© 2025 Samuele Inc.'**
  String get aboutCopyright;

  /// Logout button text
  ///
  /// In en, this message translates to:
  /// **'Logout'**
  String get logoutTitle;

  /// Snackbar message when user logs out
  ///
  /// In en, this message translates to:
  /// **'Logged out successfully'**
  String get logoutSuccessMessage;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'it'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'it':
      return AppLocalizationsIt();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
