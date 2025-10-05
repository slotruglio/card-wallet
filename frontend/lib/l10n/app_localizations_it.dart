// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Italian (`it`).
class AppLocalizationsIt extends AppLocalizations {
  AppLocalizationsIt([String locale = 'it']) : super(locale);

  @override
  String get helloWorld => 'Ciao Mondo!';

  @override
  String get homeItem => 'Home';

  @override
  String get addItem => 'Carica';

  @override
  String get settingsItem => 'Impostazioni';

  @override
  String get noMoreGiftCardText => '🎉 Non ci sono altri buoni';

  @override
  String amountText(String amount) {
    return 'Importo: $amount';
  }

  @override
  String expirationDateText(String expirationDate) {
    return 'Scade il $expirationDate';
  }

  @override
  String get giftCardPageTitle => 'Buoni';

  @override
  String get giftCardUploadSuccessText => 'Buono caricato con successo!';

  @override
  String get giftCardUploadText => 'Carica Buono';

  @override
  String get supplierText => 'Fornitore';

  @override
  String get supplierValidationText => 'Inserisci il nome del fornitore';

  @override
  String get amountFormText => 'Importo';

  @override
  String get amountValidationText => 'Inserisci importo';

  @override
  String get amountWrongText => 'Inserisci un numero valdio';

  @override
  String get expirationDateFormText => 'Data di scadenza';

  @override
  String get expirationDateFormTooltip => 'Fai tap per selezionare la data';

  @override
  String get fileFormText => 'Scegli file';

  @override
  String get uploadingText => 'Caricando...';

  @override
  String get uploadGiftCardButtonText => 'Carica buono';
}
