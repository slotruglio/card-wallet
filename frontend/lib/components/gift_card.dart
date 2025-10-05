
import 'package:card_wallet/l10n/app_localizations.dart';
import 'package:flutter/material.dart';

class GiftCardData {
  final String id;
  final String supplier;
  final double amount;
  final DateTime? expirationDate;
  
  GiftCardData(this.id, this.supplier, this.amount, this.expirationDate);
}

// --------------------- Detail View ---------------------
class GiftCardDetailView extends StatelessWidget {
  final GiftCardData giftCard;
  final VoidCallback onBack;

  const GiftCardDetailView({super.key, required this.giftCard, required this.onBack});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(giftCard.supplier, style: const TextStyle(fontSize: 18)),
          const SizedBox(height: 8),
          Text(AppLocalizations.of(context)!.amountText(giftCard.amount.toStringAsFixed(2)), style: const TextStyle(fontSize: 18)),          const SizedBox(height: 8),
          const SizedBox(height: 8),
          Text(AppLocalizations.of(context)!.expirationDateText(giftCard.expirationDate.toString()), style: const TextStyle(fontSize: 18)),
        ],
      ),
    );
  }
}
