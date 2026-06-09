import os
from groq import Groq


def groq_ai_insight(workouts: list, nutrition: dict, measurements: list) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    workout_lines = []
    for w in workouts[:5]:
        if w.get("exercises"):
            ex_names = ", ".join(e.get("ad", "") for e in w["exercises"])
            workout_lines.append(f"- {w.get('date', 'tarih yok')}: {ex_names}")
    workout_summary = "\n".join(workout_lines) if workout_lines else "Antrenman verisi yok"

    avg_kal  = nutrition.get("avg_kalori", 0)
    avg_prot = nutrition.get("avg_protein", 0)
    nutr_line = (
        f"Gunluk ort. kalori: {avg_kal} kcal, protein: {avg_prot}g"
        if (avg_kal or avg_prot) else "Beslenme verisi girilmemiş"
    )

    meas_line = ""
    if measurements:
        m = measurements[0]
        meas_line = f"Son vücut ölçümü: {m.get('weight', '?')} kg"
        if m.get("fat"):
            meas_line += f", %{m['fat']} yağ oranı"

    prompt = f"""Sen SportakipAI'ın kişisel fitness koçusun. Kullanıcının verilerini analiz et.

Son antrenmanlar:
{workout_summary}

Beslenme:
{nutr_line}

{('Vücut: ' + meas_line) if meas_line else ''}

Lütfen şunları yaz:
1. Kısa genel değerlendirme (2-3 cümle)
2. Bu hafta için 3 somut öneri (numaralı liste)
3. Kısa motivasyon cümlesi

Türkçe yaz. Samimi, motive edici ve net ol. Maksimum 250 kelime."""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Sen SportakipAI fitness uygulamasının AI koçusun. Her zaman Türkçe konuş, samimi ve motive edici ol."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-8b-instant",
        max_tokens=600,
        temperature=0.8,
    )

    return response.choices[0].message.content


def groq_ai_chat(message: str, history: list, context: dict) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    ctx_parts = []
    if context.get("profile"):
        ctx_parts.append(f"Kullanıcı profili: {context['profile']}")
    if context.get("recent_workouts"):
        ctx_parts.append(f"Son antrenmanlar: {context['recent_workouts']}")
    if context.get("nutrition"):
        ctx_parts.append(f"Bugünkü beslenme: {context['nutrition']}")
    if context.get("measurements"):
        ctx_parts.append(f"Son vücut ölçümü: {context['measurements']}")
    if context.get("goals"):
        ctx_parts.append(f"Hedefler: {context['goals']}")
    ctx_str = "\n".join(ctx_parts) if ctx_parts else "Henüz veri girilmemiş."

    system_content = f"""Sen SportakipAI'ın kişisel fitness koçusun.

Kullanıcı verileri özeti:
{ctx_str}

Kurallar:
- Her zaman Türkçe cevap ver.
- Antrenman, beslenme ve fiziksel gelişim odaklı kal.
- Kısa, net ve uygulanabilir öneriler ver (max 150 kelime).
- Tıbbi teşhis, ilaç, doping veya hastalık tedavisi önerme.
- Veri yoksa bunu belirt ve kullanıcıdan veri girmesini iste.
- Samimi ve motive edici ol."""

    messages = [{"role": "system", "content": system_content}]
    for h in history[-10:]:
        if h.get("role") in ("user", "assistant") and h.get("content"):
            messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        messages=messages,
        model="llama-3.1-8b-instant",
        max_tokens=400,
        temperature=0.7,
    )

    return response.choices[0].message.content