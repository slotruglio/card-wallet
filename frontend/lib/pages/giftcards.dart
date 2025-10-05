import 'package:card_wallet/components/gift_card.dart';
import 'package:card_wallet/l10n/app_localizations.dart';
import 'package:flutter/material.dart';

// --------------------- Page Types ---------------------
enum PageType { list, details }

class PageState {
  final PageType type;
  final String? cardId; // only used for details
  PageState(this.type, {this.cardId});
}

// --------------------- Main Page ---------------------
class GiftCardPage extends StatefulWidget {
  const GiftCardPage({super.key});

  @override
  State<GiftCardPage> createState() => _GiftCardPageState();
}

class _GiftCardPageState extends State<GiftCardPage> {
  final List<PageState> pageStack = [PageState(PageType.list)];

  // Mock gift cards
  final List<GiftCardData> giftCards = List.generate(
      20,
      (index) => GiftCardData(
        '$index',
        'Supplier $index',
        (index + 1) * 100,
        null
        ));

  @override
  Widget build(BuildContext context) {
    final current = pageStack.last;

    return WillPopScope(
      onWillPop: () async {
        if (pageStack.length > 1) {
          setState(() => pageStack.removeLast());
          return false;
        }
        return true;
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text(AppLocalizations.of(context)!.giftCardPageTitle),
          leading: pageStack.length > 1
              ? IconButton(
                  icon: const Icon(Icons.arrow_back),
                  onPressed: () {
                    setState(() => pageStack.removeLast());
                  },
                )
              : null,
        ),
        body: _buildCurrentPage(current),
      ),
    );
  }

  Widget _buildCurrentPage(PageState current) {
    switch (current.type) {
      case PageType.list:
        return GiftCardListView(
          giftCards: giftCards,
          onCardTap: (id) {
            setState(() => pageStack.add(PageState(PageType.details, cardId: id)));
          },
        );
      case PageType.details:
        final card =
            giftCards.firstWhere((c) => c.id == current.cardId, orElse: () => GiftCardData('0', 'Unknown', 0, null));
        return GiftCardDetailView(
          giftCard: card,
          onBack: () => setState(() => pageStack.removeLast()),
        );
    }
  }
}

// --------------------- List View ---------------------
class GiftCardListView extends StatelessWidget {
  final List<GiftCardData> giftCards;
  final void Function(String cardId) onCardTap;

  const GiftCardListView({
    super.key,
    required this.giftCards,
    required this.onCardTap,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: giftCards.length,
      itemBuilder: (context, index) {
        final card = giftCards[index];
        return ListTile(
          title: Text(card.supplier),
          subtitle: Text(AppLocalizations.of(context)!.amountText(card.amount.toStringAsFixed(2))),
          onTap: () => onCardTap(card.id),
        );
      },
    );
  }
}
