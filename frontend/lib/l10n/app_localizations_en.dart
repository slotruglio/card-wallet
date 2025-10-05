// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get helloWorld => 'Hello World!';

  @override
  String get homeItem => 'Home';

  @override
  String get addItem => 'Add';

  @override
  String get settingsItem => 'Setting';

  @override
  String get noMoreGiftCardText => '🎉 No more gift cards';

  @override
  String amountText(String amount) {
    return 'Amount: $amount';
  }

  @override
  String expirationDateText(String expirationDate) {
    return 'Expires on $expirationDate';
  }

  @override
  String get giftCardPageTitle => 'Gift Cards';

  @override
  String get giftCardUploadSuccessText => 'Gift card uploaded successfully!';

  @override
  String get giftCardUploadText => 'Upload Gift Card';

  @override
  String get supplierText => 'Supplier';

  @override
  String get supplierValidationText => 'Enter supplier name';

  @override
  String get amountFormText => 'Amount';

  @override
  String get amountValidationText => 'Enter amount';

  @override
  String get amountWrongText => 'Enter a valid number';

  @override
  String get expirationDateFormText => 'Expiration Date';

  @override
  String get expirationDateFormTooltip => 'Tap to select date';

  @override
  String get fileFormText => 'Select File';

  @override
  String get uploadingText => 'Uploading...';

  @override
  String get uploadGiftCardButtonText => 'Upload Gift Card';
}
