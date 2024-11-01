from dataclasses import dataclass
@dataclass
class Vacancy():
    name: str = None
    salaryzMin: str = None
    salaryzMax: str = None
    valuta: str = None
    refVacancy: str = None
    refSite: str = 'https://novosibirsk.hh.ru'

    def to_dict(self):
        return {
            'name': self.name,
            'salaryzMin': self.salaryzMin,
            'salaryzMax': self.salaryzMax,
            'valuta': self.valuta,
            'refVacancy': self.refVacancy,
            'refSite': self.refSite
        }