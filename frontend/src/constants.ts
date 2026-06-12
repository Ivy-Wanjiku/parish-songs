export const MISAS = [
  { id: 'banana', name: 'Misa Banana' },
  { id: 'subukia', name: 'Misa Subukia' },
  { id: 'taita', name: 'Misa Taita' },
  { id: 'amecea', name: 'Misa AMECEA' },
  { id: 'other', name: 'Other Misa' },
] as const;

export const PROPER_CATEGORIES = [
  'Entrance',
  'Bible Procession',
  'Offertory',
  'Communion',
  'Thanksgiving',
  'Recessional',
  'Responsorial Psalm',
] as const;

export const ORDINARY_PARTS = [
  { id: 'ord-Kyrie', name: 'Kyrie' },
  { id: 'ord-Gloria', name: 'Gloria' },
  { id: 'ord-Sanctus', name: 'Sanctus' },
  { id: 'ord-Agnus Dei', name: 'Agnus Dei' },
  { id: 'ord-Other', name: 'Other' },
] as const;

export const LANGUAGES = ['Swahili', 'Kikuyu', 'English', 'Latin', 'Other'] as const;

export const CATEGORY_LABELS: Record<string, string> = {
  Entrance: 'Entrance',
  'Bible Procession': 'Bible Procession',
  Offertory: 'Offertory',
  Communion: 'Communion',
  Thanksgiving: 'Thanksgiving',
  Recessional: 'Recessional',
  'Responsorial Psalm': 'Responsorial Psalm',
  'ord-Kyrie': 'Kyrie',
  'ord-Gloria': 'Gloria',
  'ord-Sanctus': 'Sanctus',
  'ord-Agnus Dei': 'Agnus Dei',
  'ord-Other': 'Other',
};

/** Colour dot per category */
export const CAT_COLORS: Record<string, string> = {
  Entrance: '#C9A84C',
  'Bible Procession': '#7BA7BC',
  Offertory: '#A08060',
  Communion: '#9B7BAA',
  Thanksgiving: '#6FAA7B',
  Recessional: '#AA7B7B',
  'Responsorial Psalm': '#7B95AA',
  'ord-Kyrie': '#E2C97E',
  'ord-Gloria': '#F0DFA0',
  'ord-Sanctus': '#E2C97E',
  'ord-Agnus Dei': '#F0DFA0',
  'ord-Other': '#C9A84C',
};

export const ALL_CATEGORY_ORDER = [
  ...PROPER_CATEGORIES,
  ...ORDINARY_PARTS.map((p) => p.id),
];
