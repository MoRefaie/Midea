"""Midea Extras sensors."""

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "midea_extras"


@dataclass(frozen=True, kw_only=True)
class ExtraSensorDescription(SensorEntityDescription):
    """Midea extra sensor description."""


SENSORS = [
    ExtraSensorDescription(
        key="temp_t3",
        name="T3 Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensors."""

    midea_entries = hass.config_entries.async_entries("midea")

    entities = []

    for midea_entry in midea_entries:
        device = getattr(midea_entry, "runtime_data", None)

        if device is None:
            continue

        entities.extend(
            MideaExtraSensor(device, description)
            for description in SENSORS
            if device.attributes.get(description.key) is not None
        )

    async_add_entities(entities)


class MideaExtraSensor(SensorEntity):
    """Midea Extra Sensor."""

    def __init__(self, device, description):
        self._device = device
        self.entity_description = description

        self._attr_unique_id = (
            f"{device.device_id}_{description.key}"
        )

        self._attr_name = description.name

    @property
    def native_value(self):
        return self._device.get_attribute(
            self.entity_description.key
        )

    @property
    def device_info(self):
        return {
            "identifiers": {
                ("midea", str(self._device.device_id))
            }
        }