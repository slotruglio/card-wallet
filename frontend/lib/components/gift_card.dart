
import 'package:card_wallet/l10n/app_localizations.dart';
import 'package:flutter/material.dart';

class GiftCardData {
  final String supplier;
  final double amount;
  final DateTime expirationDate;

  GiftCardData(this.supplier, this.amount, this.expirationDate);
}

class GiftCardWidget extends StatelessWidget {
  const GiftCardWidget({super.key, required this.data});

  final GiftCardData data;

  @override
  Widget build(BuildContext context) {
    return Card(
              margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              child: ListTile(
                title: Text(data.supplier),
                subtitle: Text(
                  "${AppLocalizations.of(context)!.amountText(data.amount.toStringAsFixed(2))}\n${AppLocalizations.of(context)!.expirationDateText(data.expirationDate.toLocal().toString().split(' ')[0])}"
                ),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
              ),
            );
  }
}