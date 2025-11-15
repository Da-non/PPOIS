class SoundDesigner(GameEntity):
    """
    Класс звукового дизайнера.
    
    Attributes:
        sound_designer_id (str): Уникальный идентификатор дизайнера
        created_sounds (Dict): Созданные звуковые эффекты
        background_music (List): Фоновая музыка
        voice_overs (Dict): Озвучка
    """

    def __init__(self, sound_designer_id: str, name: str):
        super().__init__(sound_designer_id, name)
        self.created_sounds = {}
        self.background_music = []
        self.voice_overs = {}
        self.audio_mix = {}
        self.specialization = "sfx"  # sfx, music, voice, mixing

    def update(self, delta_time: float) -> None:
        """Обновляет состояние звукового дизайнера."""
        pass

    def create_sound_effect(self, sound_id: str, name: str, category: str,
                           file_path: str, duration: float) -> Dict[str, Any]:
        """Создает звуковой эффект."""
        sound_effect = {
            "sound_id": sound_id,
            "name": name,
            "category": category,  # weapon, environment, ui, etc.
            "file_path": file_path,
            "duration": duration,
            "created_at": datetime.now(),
            "designer": self.entity_id,
            "volume": 1.0,
            "spatial_blend": 1.0  # 3D sound
        }
        
        self.created_sounds[sound_id] = sound_effect
        return sound_effect

    def add_background_music(self, track_id: str, title: str, composer: str,
                           file_path: str, duration: float, mood: str) -> Dict[str, Any]:
        """Добавляет фоновую музыку."""
        music_track = {
            "track_id": track_id,
            "title": title,
            "composer": composer,
            "file_path": file_path,
            "duration": duration,
            "mood": mood,  # peaceful, intense, mysterious, etc.
            "added_at": datetime.now(),
            "volume": 0.8,
            "loop": True
        }
        
        self.background_music.append(music_track)
        return music_track

    def record_voice_over(self, voice_id: str, character_id: str, lines: List[Dict],
                        voice_actor: str) -> Dict[str, Any]:
        """Записывает озвучку."""
        voice_over = {
            "voice_id": voice_id,
            "character_id": character_id,
            "lines": lines,
            "voice_actor": voice_actor,
            "recorded_at": datetime.now(),
            "designer": self.entity_id,
            "language": "russian"
        }
        
        self.voice_overs[voice_id] = voice_over
        return voice_over

    def create_audio_mix(self, mix_id: str, settings: Dict) -> Dict[str, Any]:
        """Создает аудио-микс."""
        audio_mix = {
            "mix_id": mix_id,
            "settings": settings,
            "created_at": datetime.now(),
            "designer": self.entity_id,
            "master_volume": settings.get("master_volume", 1.0),
            "music_volume": settings.get("music_volume", 0.8),
            "sfx_volume": settings.get("sfx_volume", 1.0),
            "voice_volume": settings.get("voice_volume", 1.0)
        }
        
        self.audio_mix[mix_id] = audio_mix
        return audio_mix

