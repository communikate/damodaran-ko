---
layout: post
title: "2025년 데이터 업데이트 1: 데이터의 매력(과 위험)"
date: 2025-01-10
original_title: "Data Update 1 for 2025: The Draw (and Danger) of Data"
original_url: "https://aswathdamodaran.blogspot.com/2025/01/data-update-1-for-2025-draw-and-danger.html"
original_author: "Aswath Damodaran"
categories: [translation, finance]
comments: false
---

지난 40년 동안, 저는 매년 초 첫째 주를 상장 기업 데이터를 수집·분석하고 그 결과를 관심 있는 모든 분과 공유하는 데 사용해 왔습니다. 2025년의 첫 전체 주가 끝났고, [올해의 데이터 업데이트](https://pages.stern.nyu.edu/~adamodar/data.html)가 이제 가동을 시작했습니다. 이번 포스팅에서는 제 데이터 샘플, 산업 통계 산출 방식, 그리고 데이터에 접근하는 방법을 설명하겠습니다. 또한 데이터가 어떻게, 어디에 활용하기에 가장 적합한지에 관해 항상 덧붙여 온 주의사항도 반복하겠습니다.

## 데이터의 매력(과 위험)

데이터의 시대입니다. 기업과 투자자 모두 데이터를 길들여 상업적 이익에 활용하고 있다고 주장합니다. 저는 데이터가 더 나은 의사결정으로 이어질 수 있다고 믿지만, 의사결정 최적화와 관련하여 데이터가 할 수 있는 것과 할 수 없는 것에 대한 주장들을 경계합니다. 데이터의 가장 큰 활용 가치는 두 가지 차원에서 발휘된다고 생각합니다:

1. *주장 사실 확인*: 인간이 신념을 사실로 주장하는 것은 언제나 있어 왔지만, 소셜 미디어 시대에는 훨씬 더 많은 청중에게 그 주장을 전달할 수 있게 되었습니다. 제가 일하는 기업 재무와 투자 분야에서, 저는 정치인·시장 전문가·경제학자들이 기업과 시장 행태에 관해 마치 동화 같은 이야기를 사실처럼 말하는 것을 들으며 이중으로 놀라곤 합니다. 데이터는 종종 진실을 가려내는 제 무기가 됩니다.

2. *예측의 불확실성*: 전문가 집단이 점점 불신받는 이유 중 하나는, 이 집단 중 많은 이들이 미래 예측의 불확실성을 인정하지 않으려는 태도 때문입니다. 학문적·직업적 자격증 뒤에 숨어 자신들이 옳다는 믿음을 요구하지만, 그 신뢰는 이미 침식되었습니다. 이러한 예측들이 데이터에 기반한다고 주장한다면, 거의 예외 없이 오차(노이즈)가 수반되며, 이를 인정하는 것은 약함의 표시가 아닙니다. 때로는 오차의 규모가 너무 커서 예측을 듣는 사람들이 행동에 옮기지 못할 수 있지만, 그것은 오히려 건강한 반응입니다.

많은 이들이 AI와 분석 기술의 매력이 더해지면서 데이터의 주문에 걸리는 것을 보면서, 저는 데이터가 모든 답을 가지고 있다는 생각에 불편함을 느낍니다. 그 이유는 두 가지입니다:

1. *데이터는 편향될 수 있습니다*: 데이터는 객관적이라는 믿음이 널리 퍼져 있습니다. 적어도 수치 형태를 띠고 있다면 그렇다는 것입니다. 그러나 편향되거나 특정 목적을 가진 분석가의 손에서 데이터는 선입관에 맞게 조작될 수 있습니다. 저 역시 편향이 없다고 주장하고 싶지만 그것은 거짓말이 될 것입니다. 편향은 종종 깊이 박혀 있고 무의식적이기 때문입니다. 다만 저는 사용하는 샘플, 작업하는 데이터, 통계를 계산하는 방식에 대해 최대한 투명하게 공개하려 노력해 왔습니다. 정밀도를 추구하는 분들에게는 답답할 수 있습니다만, 서로 다른 샘플링과 추정 방식에 따른 값의 범위를 제시하기 때문입니다. 2025년 초 미국 기업들의 산업별 세율 계산을 살펴보면 다음과 같습니다.

[![유효세율(미국)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi7VcXRHtktOKA5AAoF6tPfKutcUqEV7_f_qK1xNqeUgvasUC06wy6KSFd720du8TpqQKk2uWyeCSiOvD3hkuFZXQL15VVREjrSDCk2vaSZ9qTUsO5Z_AAwEyjsbx1fsBJWxJT9Bo7Y0kz4PKgWPH4orDYD6kV5uLHRoMOK6vCgAZeuwxuCjBEft5ndik4/w400-h293/EffTaxRateUS.jpeg)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi7VcXRHtktOKA5AAoF6tPfKutcUqEV7_f_qK1xNqeUgvasUC06wy6KSFd720du8TpqQKk2uWyeCSiOvD3hkuFZXQL15VVREjrSDCk2vaSZ9qTUsO5Z_AAwEyjsbx1fsBJWxJT9Bo7Y0kz4PKgWPH4orDYD6kV5uLHRoMOK6vCgAZeuwxuCjBEft5ndik4/s1478/EffTaxRateUS.jpeg)

*[산업별 유효세율 (미국)](https://pages.stern.nyu.edu/~adamodar/pc/datasets/taxrate.xls)*

미국 기업의 세율은 계산 방식과 사용하는 기업 샘플에 따라 6.75%에서 26.43%까지 분포합니다. 미국 기업들이 세금을 공정하게 부담하지 않는다는 선입관을 가진 분이라면 6.75%를 선택할 것이고, 공정하게(또는 그 이상) 부담한다고 생각하는 분이라면 26.43%를 선호할 것입니다.

2. *과거 대 미래*: 투자자와 기업들은 종종 미래 예측을 과거에 근거합니다. 이는 충분히 이해할 수 있지만, 모든 투자 설명서에 "과거 성과는 미래 성과의 신뢰할 만한 지표가 아닙니다"라는 면책 조항이 붙어 있는 이유가 있습니다. [저는 평균 회귀(mean reversion)가 많은 적극적 투자 전략의 핵심에 있으며, 역사가 반복될 것이라는 가정이 잘못될 수 있음을 글로 쓴 바 있습니다](https://aswathdamodaran.blogspot.com/2016/08/mean-reversion-gravitational-super.html). 따라서 제가 제공하는 시간에 따른 내재 주식위험프리미엄(ERP) 또는 S&P 500의 PER 과거 데이터를 살펴보면서 평균을 계산해 투자 전략에 활용하거나, 산업 평균 부채비율·가격 배수를 동종업계 모든 기업의 목표치로 삼고 싶어질 수 있습니다. 그러나 조금만 참아주십시오.

## 샘플

데이터가 이전 어느 때보다 접근하기 쉽고 풍부해졌다는 것은 부인할 수 없으며, 저도 그 혜택을 받고 있습니다. 저는 여러 원시 데이터 소스에서 데이터를 가져옵니다. 일부는 누구에게나 무료이고, 일부는 제가 비용을 지불하며, 일부는 대학 경영대학원에 재직하는 덕분에 접근할 수 있습니다. 기업 데이터의 주요 소스는 S&P Capital IQ이며, Bloomberg 터미널 데이터로 보완합니다. 거시경제 데이터의 주요 소스는 [FRED (연방준비은행이 관리하는 데이터셋)](https://fred.stlouisfed.org)이지만, 채권 스프레드 데이터를 위한 [NAIC](https://content.naic.org)와 국가 위험 점수를 위한 [Political Risk Services (PRS)](https://www.prsgroup.com) 등 온라인에서 찾은 다른 데이터로 보완합니다.

저의 데이터셋은 연초 기준으로 시장 가격이 있는 모든 상장 기업을 포함하며, **2025년 샘플에는 47,810개 기업**이 포함되어 최근 몇 년의 샘플 규모와 비슷합니다. 기업 목록은 전 세계에 걸쳐 있으며, 지역별 기업 수와 시가총액 분포는 다음과 같습니다:

[![샘플 파이차트](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjTJoXsEj_eMisIAMS_TwpjR-ZeuGs8bLSOGaH6Z5wxjz29zw3SIhfo-ZbvDQyuUFTkUuEjdur3LyUH37-P2AuC03cmvL2ApWpt1NY7Y4rNnDEc2pe3xCFsR3QldPogvdg3cY_SFJ-DszQTpYHa8pSj_sjpyw_albxzTHVnVNteDO2ttDlnzFo8iWh1CHM/w271-h400/SamplePie.jpeg)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjTJoXsEj_eMisIAMS_TwpjR-ZeuGs8bLSOGaH6Z5wxjz29zw3SIhfo-ZbvDQyuUFTkUuEjdur3LyUH37-P2AuC03cmvL2ApWpt1NY7Y4rNnDEc2pe3xCFsR3QldPogvdg3cY_SFJ-DszQTpYHa8pSj_sjpyw_albxzTHVnVNteDO2ttDlnzFo8iWh1CHM/s1824/SamplePie.jpeg)

보시다시피, 2025년 초 미국 기업의 시가총액은 전 세계 주식 시가총액의 약 49%를 차지했는데, 이는 2024년 초의 44%, 2023년 초의 42%에서 상승한 수치입니다. 아래 표는 시간에 따른 지역별 시가총액(단위: 백만 달러) 변화를 비교합니다.

[![지역별 시가총액 추이](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhkh-QCT7r8-RyoAPkESsIzJx9lT6WiMk-80SeGKOeJBvKs4nA0kejVA0g6cSi06zkdeXOFSIrYYeHfMOlAe0bAnE7_WaotD88CpZm81THpL8LnxNgiYXCtun2icnWUvV6YfIpdDQkLLlPOkxuaASXnv4twPUhxZierTDfU8HumcWCXpmwZcPNt8RwIpmM/w400-h171/Regionaovertime.jpeg)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhkh-QCT7r8-RyoAPkESsIzJx9lT6WiMk-80SeGKOeJBvKs4nA0kejVA0g6cSi06zkdeXOFSIrYYeHfMOlAe0bAnE7_WaotD88CpZm81THpL8LnxNgiYXCtun2icnWUvV6YfIpdDQkLLlPOkxuaASXnv4twPUhxZierTDfU8HumcWCXpmwZcPNt8RwIpmM/s1156/Regionaovertime.jpeg)

(S&P) 섹터별로 기업을 분류하면 다음과 같습니다:

[![섹터 파이차트](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiBwjkcqLmL11qP7wtsb70iC9Am292l1Jer5iESDg3F5eVADqM41Ye-WyuMbrU_hh1iCSunBV2hi2tOrzBUJBE9IWtY247W9IsDDIlK8BQkyGhKjvGFP_n7uFGjlHkkyvHqbGF3BE1UQxJR-voGghktSWA5FrChpk_cd0LHRzc9R5POhrV44no7Me7RyPE/w275-h400/SectorPie.jpeg)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiBwjkcqLmL11qP7wtsb70iC9Am292l1Jer5iESDg3F5eVADqM41Ye-WyuMbrU_hh1iCSunBV2hi2tOrzBUJBE9IWtY247W9IsDDIlK8BQkyGhKjvGFP_n7uFGjlHkkyvHqbGF3BE1UQxJR-voGghktSWA5FrChpk_cd0LHRzc9R5POhrV44no7Me7RyPE/s1566/SectorPie.jpeg)

상장 종목 수는 산업재(Industrials)가 가장 많지만, 기술(Technology) 섹터가 전 세계 상장 주식 시가총액의 21%를 차지해 가장 높은 가치를 지닌 섹터입니다. 섹터 구성은 지역에 따라 큰 차이를 보입니다:

[![지역별 섹터 비중](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjz4nMXdWZpWFd66exYQINpJeNNEq2uMstZgnge5HM1ar4zaiiuhGzf_nmGMoU0cZjtmmUDbfXrZyGF6Dg9m7CSbuRQ5OaGgKGkCYBXjwojFJEQ9-dgMoWcJdOhFVuXbBkXNAB3J9hiMZSaf0XMc90p7mbIvpbCQU79YUQyldiE4AKuQ3-ZVwpZtjNJydU/w400-h88/SectorbyRegionTable.jpeg)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjz4nMXdWZpWFd66exYQINpJeNNEq2uMstZgnge5HM1ar4zaiiuhGzf_nmGMoU0cZjtmmUDbfXrZyGF6Dg9m7CSbuRQ5OaGgKGkCYBXjwojFJEQ9-dgMoWcJdOhFVuXbBkXNAB3J9hiMZSaf0XMc90p7mbIvpbCQU79YUQyldiE4AKuQ3-ZVwpZtjNJydU/s1754/SectorbyRegionTable.jpeg)

미국 주식 시가총액 증가의 상당 부분은 기술 섹터의 급성장에서 비롯되었으며, 유럽은 이 표의 모든 대형 서브그룹 중 기술 기업 비중이 가장 낮다는 점이 인상적입니다.

저는 또한 기업들을 94개 산업 그룹으로 더 세분화하여 분류합니다. 이 분류 체계는 1990년대에 Value Line 데이터를 기반으로 제가 직접 만든 산업 분류를 느슨하게 유지한 것으로, 시간에 따른 비교를 가능하게 합니다. SIC나 NAICS 코드 기반의 산업 분류와는 다르지만, 기업 재무와 밸류에이션 맥락에서는 충분히 잘 작동합니다. 저의 산업 분류가 지나치게 넓다고 느끼는 분들도 계시겠지만, 더 세밀한 동종업계 집단이 필요하다면 다른 곳에서 찾아보셔야 할 것 같습니다. 제가 보고하는 산업 평균은 위에서 설명한 지역별 분류를 사용하여 제공됩니다. 어떤 기업이 어느 산업 그룹에 속하는지 확인하려면 [이 파일을 클릭](https://pages.stern.nyu.edu/~adamodar/pc/datasets/indname.xlsx)하십시오(다운로드에 시간이 다소 걸릴 수 있는 대용량 파일입니다).

## 변수

제가 산업 평균 통계를 보고하는 변수들은 제 관심사를 반영하며, 위험, 수익성, 레버리지, 배당 지표 등 다양한 범위에 걸쳐 있습니다. 기업 재무와 밸류에이션을 가르치는 입장에서, 이 데이터를 투자(Investing), 자금조달(Financing), 배당(Dividends)이라는 기업 의사결정 그룹으로 분류하여 제공하는 것이 유용하다고 생각합니다([2025년 미국 데이터 링크가 포함되어 있으며, 더 광범위한 데이터 링크는 여기에서](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html) 확인하실 수 있습니다).

이들 기업 재무 변수 중 많은 것들—자기자본비용(Cost of Equity)·자본비용(WACC), 부채비율, 회계적 수익률 등—이 밸류에이션에도 활용되며, 밸류에이션 및 가격결정 데이터 필요에 맞춘 변수들도 추가됩니다.

*(링크가 작동하지 않으면 다른 브라우저를 사용해 보십시오.)*

이 데이터 중 상당 부분은 재무제표에서 도출되지만, 일부는 시장 가격 기반(베타, 표준편차, 거래 데이터)이고, 일부는 자산 클래스(주식·채권·부동산 수익률)에 관한 것이며, 일부는 거시경제적(금리, 인플레이션, 위험프리미엄)입니다. 일부 변수는 명확하지만 다른 것들은 해석의 여지가 있으므로, 회계 변수의 정의를 확인할 수 있는 [용어집](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/definitions.html)을 제공합니다. 또한 각 데이터셋(엑셀 형식) 내에 해당 데이터셋에서 사용된 변수를 정의하는 페이지가 있습니다.

## 데이터 기준 시점

이 데이터셋들은 모두 지난 나흘간 수집된 것으로, 2025년 초에 이용 가능한 데이터를 반영합니다. 시가총액, 금리, 위험프리미엄과 같은 시장 수치는 **2025년 초의 시장 판단을 반영**하는 현재 데이터입니다. 기업 재무 수치의 경우 분기별로 업데이트되는 회계 정보에 의존하므로, **회계 수치는 가장 최근의 재무 보고(통상 2024년 9월 30일 기준)**를 반영하며, 유동 수치(손익계산서·현금흐름표)는 가장 최근 신고까지의 최근 12개월 수치를, 재고 수치(대차대조표 값)는 가장 최근의 대차대조표를 사용합니다.

이 관행이 일관성이 없어 보일 수 있지만, 이는 시장의 투자자들이 실제로 주식 가격을 결정할 때 이용할 수 있는 정보를 반영한 것입니다. 어떤 투자자도 2025년 초에 2024년 연간 회계 수치에 접근할 수 없으며, 2025년 초의 후행 PER(Trailing P/E)을 2025년 초 주가를 2024년 9월까지 12개월간의 후행 순이익으로 나누어 계산하는 것은 완전히 합리적입니다. 같은 맥락에서, 미래 예상 성장률과 미래 연도 이익은 2025년 초 기준 애널리스트들의 가장 최신 예측을 참조합니다.

저는 연 1회만 데이터를 업데이트하므로, 2025년이 진행될수록 데이터는 낡아지겠지만, 이는 회계 비율보다 가격 배수(PER, PBR, EV/EBITDA 등)를 사용하는 경우에 더 크게 느껴질 것입니다. 금리와 위험프리미엄이 연중 변화할 수 있으므로, 이를 사용하는 데이터셋(자본비용, 초과 수익률)은 이러한 거시 수치를 업데이트할 수 있도록 설계되어 있습니다. 즉, 10년 만기 국채 금리가 5%로 오르고 주식위험프리미엄(ERP)이 급등한다면, [자본비용 워크시트](https://pages.stern.nyu.edu/~adamodar/pc/datasets/wacc.xls)에서 해당 수치를 업데이트하여 최신 값을 얻을 수 있습니다.

## 추정 방법론

저는 기업별로 데이터 변수를 계산하지만, 원시 데이터 제공자의 제약으로 기업별 데이터는 공유하기 어렵고, 대부분의 데이터는 산업 수준에서 보고됩니다. 그런데 거의 모든 통계 측정 방법에는 주의사항이 있기 때문에, 산업 통계를 어떻게 추정하고 보고할지 고민해 왔습니다. 예를 들어 PER의 경우, 기업들의 단순 평균을 내면 적자 기업을 제외함으로 인한 표본 편향이 발생하고 이상치에 의해 한쪽 방향으로 왜곡됩니다(PER은 음수가 될 수 없으므로 주로 양의 방향). 이 문제가 거의 모든 변수에서 발생하므로, 저는 집계 방식을 사용합니다. PER의 경우, 산업 그룹 내 모든 기업(적자 기업 포함)의 시가총액을 합산하고 이를 모든 기업(적자 기업 포함)의 합산 순이익으로 나누는 방식입니다.

샘플에 모든 상장 기업을 포함하지만, 공시 요건은 기업마다 다릅니다. 일부 변수에서 데이터가 누락되거나 공시되지 않는 경우가 있습니다. 이러한 기업을 샘플에서 완전히 제외하는 대신, 저는 전체 유니버스에 유지하되 비결측 데이터가 있는 기업에 대해서만 값을 보고합니다. 예를 들어 2년 전에 추가한 [직원 데이터셋](https://pages.stern.nyu.edu/~adamodar/pc/datasets/Employee.xls)은 직원 1인당 매출과 보상 통계를 보고하는데, 이는 일부 기업들이 자발적으로만 공시하는 데이터 항목이므로 보편적으로 공시되는 항목보다 통계의 신뢰도가 낮습니다.

긍정적인 측면에서, 수십 년째 이 작업을 해온 입장에서 보면, 전 세계 회계 기준이 과거보다 훨씬 덜 분산되어 있고, 소규모 신흥시장에서도 데이터의 결측 항목이 10~20년 전보다 크게 줄었습니다.

## 데이터 접근 및 활용

제 웹사이트에서 찾을 수 있는 데이터는 공개용이며, 쉽게 접근할 수 있도록 정리해 두었습니다. 현재 연도 데이터는 다음에서 확인하실 수 있습니다:

[https://pages.stern.nyu.edu/~adamodar//New_Home_Page/datacurrent.html](https://pages.stern.nyu.edu/~adamodar//New_Home_Page/datacurrent.html)

링크를 클릭해도 작동하지 않으면 다른 브라우저를 시도해 보십시오. 특히 Google Chrome은 제 서버에서 다운로드 시 문제가 발생한 경우가 있습니다.

이전 연도 데이터에 관심이 있다면, 제 웹페이지의 아카이브 데이터 섹션에서 확인하실 수 있습니다:

[https://pages.stern.nyu.edu/~adamodar//New_Home_Page/dataarchived.html](https://pages.stern.nyu.edu/~adamodar//New_Home_Page/dataarchived.html)

이 데이터는 미국 데이터의 경우 일부 항목은 20년 이상, 글로벌 시장은 약 10년치가 제공됩니다.

마지막으로, 이 데이터는 기업 재무와 밸류에이션 실무자들을 위한 것이며, 실시간 밸류에이션에 시간을 절약하고 도움이 되기를 바랍니다. 제 페이지의 모든 데이터 항목은 공개 소스에서 가져온 것이며, 시간과 데이터 접근성만 갖추면 누구든 재현할 수 있다는 점을 강조하고 싶습니다. 데이터 활용에 관한 전체 안내는 다음 링크를 참조하십시오:

[https://pages.stern.nyu.edu/~adamodar//New_Home_Page/datahistory.html](https://pages.stern.nyu.edu/~adamodar//New_Home_Page/datahistory.html)

규제 또는 법적 분쟁 중이고 제 데이터를 근거로 사용하신다면 환영합니다. 다만 저를 그 싸움에 끌어들이지는 말아 주십시오. 데이터 활용 시 출처를 밝혀 주신다면 감사하지만, 생략하더라도 저는 섭섭하게 생각하지 않으며 법적 경고를 하지도 않겠습니다.

마지막으로, 저는 혼자 이 작업을 합니다. 과정을 직접 통제할 수 있다는 장점이 있지만, 교황과 달리 저는 매우 오류를 범할 수 있는 사람입니다. 실수나 깨진 링크를 발견하시면 알려 주십시오. 최대한 빨리 수정하겠습니다. 또한 저는 데이터 서비스가 될 생각이 없으며, 아무리 합리적인 요청이라도 맞춤형 데이터 요청은 수용할 수 없습니다. 양해 부탁드립니다!

## YouTube 영상

<iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" height="315" referrerpolicy="strict-origin-when-cross-origin" src="https://www.youtube.com/embed/SCpqqrW-rrc?si=k1Xg1nGpq-NzQVMh" title="YouTube video player" width="560"></iframe>

## 링크

1. [최신 데이터 (2025년 초)](https://people.stern.nyu.edu/adamodar/New_Home_Page/datacurrent.html)
2. [아카이브 데이터 (이전 연도)](https://people.stern.nyu.edu/adamodar/New_Home_Page/dataarchived.html)
3. [기업/산업 분류](https://pages.stern.nyu.edu/~adamodar/pc/datasets/indname.xlsx)
4. [데이터 정의](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/definitions.html)

## 2025년 데이터 업데이트 시리즈

1. [2025년 데이터 업데이트 1: 데이터의 매력(과 위험)!](https://aswathdamodaran.blogspot.com/2025/01/data-update-1-for-2025-draw-and-danger.html)
2. [2025년 데이터 업데이트 2: 미국 주식시장의 파티는 계속됐다](https://aswathdamodaran.blogspot.com/2025/01/data-update-2-for-2025-party-continued.html)
3. [2025년 데이터 업데이트 3: 세상은 변하고 있다!](https://aswathdamodaran.blogspot.com/2025/01/data-update-3-for-2025-slicing-and.html)
4. [2025년 데이터 업데이트 4: 금리, 인플레이션, 그리고 중앙은행!](https://aswathdamodaran.blogspot.com/2025/01/data-update-4-for-2025-interest-rates.html)
5. [2025년 데이터 업데이트 5: 세상은 좁다!](https://aswathdamodaran.blogspot.com/2025/02/data-update-5-for-2025-its-small-world.html)
6. [2025년 데이터 업데이트 6: 거시에서 미시로 - 허들 레이트 문제!](https://aswathdamodaran.blogspot.com/2025/02/data-update-6-for-2025-from-macro-to.html)
7. [2025년 데이터 업데이트 7: 비즈니스의 엔드게임!](https://aswathdamodaran.blogspot.com/2025/02/data-update-7-for-2025-the-end-game-in.html)
8. [2025년 데이터 업데이트 8: 부채, 세금, 디폴트 - 불길한 삼위일체!](https://aswathdamodaran.blogspot.com/2025/02/data-update-8-for-2025-debt-taxes-and.html)
9. [2025년 데이터 업데이트 9: 배당 정책 - 관성과 모방이 지배한다!](https://aswathdamodaran.blogspot.com/2025/03/data-update-9-for-2025-dividends-and.html)

---

*이 글은 Aswath Damodaran 교수의 원문을 번역·아카이빙한 것입니다.*  
*원문: [Data Update 1 for 2025: The Draw (and Danger) of Data](https://aswathdamodaran.blogspot.com/2025/01/data-update-1-for-2025-draw-and-danger.html)*