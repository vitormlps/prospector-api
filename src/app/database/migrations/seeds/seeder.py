#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from datetime import datetime

# ### Third-party deps
from alembic import op
import sqlalchemy as sa

# ### Local deps
from app.utils.csv_readers import (
    BaysReader,
    EquipmentAnomaliesReader,
    read_equipments_coords_sheet_from_file
)
from entities.base.model import Geometry


class Seeder:
    @classmethod
    def __get_table(cls, table_name):
        return sa.Table(table_name, sa.MetaData(), autoload_with=op.get_bind())

    @classmethod
    def __get_anomalies_sheet(cls):
        return EquipmentAnomaliesReader.read_anomaly_component_sheet(
            anomalies_file="../assets/anomalies.csv",
            equipments_file="../assets/equipments_cabreuva_complete.csv"
        )

    @classmethod
    def __get_equipments_coord(cls):
        with open("../assets/ativos_cabreuva.csv") as equipment_sheet:
            with open("../assets/equipments_cabreuva_complete.csv", encoding="utf-8-sig") as equipment_extra_sheet:
                sheet_data = read_equipments_coords_sheet_from_file(
                    equipment_sheet, equipment_extra_sheet
                )
        return sheet_data

    @classmethod
    def __get_bays_information(cls):
        return BaysReader.read_bays_sheet("../assets/bays_info_cabreuva.csv")

    @classmethod
    def seed_anomalies(cls):
        table = cls.__get_table('anomaly')
        sheet_data = cls.__get_anomalies_sheet()
        data = [
            {"name": anomaly_name, "created_at": datetime.now(), "updated_at": datetime.now()}
            for anomaly_name in sheet_data["anomalies"]
        ]

        op.bulk_insert(table, data)

    @classmethod
    def seed_equipment_types(cls):
        table = cls.__get_table('equipment_type')
        sheet_data = cls.__get_anomalies_sheet()
        data = [
            {"name": equipment_type_name, "created_at": datetime.now(), "updated_at": datetime.now()}
            for equipment_type_name in sheet_data["equipments"].keys()
        ]

        op.bulk_insert(table, data)

    @classmethod
    def seed_equipments(cls):
        table = cls.__get_table('equipment')
        data = []
        conn = op.get_bind()
        equipment_type_table = cls.__get_table('equipment_type')

        sheet_data = cls.__get_equipments_coord()

        for equipment_data in sheet_data:
            equipment_type_id = conn.execute(
                sa.select(
                    equipment_type_table.columns["id"]
                ).filter(
                    equipment_type_table.columns["name"] == equipment_data["type"]
                )
            ).first()
            equipment_type_id = equipment_type_id[0] if equipment_type_id else 1
            data.append({
                "e_id": equipment_data["id"],
                "type_id": equipment_type_id,
                "updated_at": datetime.now()
            })
        else:
            conn.execute(
                sa.update(table).where(
                    table.columns["id"] == sa.bindparam("e_id")
                ).values(
                    {
                        "type_id": sa.bindparam("type_id"),
                        "updated_at": sa.bindparam("updated_at")
                    }
                ),
                data
            )

    @classmethod
    def seed_bays(cls):
        table = cls.__get_table('bay')
        data = []
        conn = op.get_bind()

        bays_information = cls.__get_bays_information()

        for bay_id, bay_name in bays_information.items():
            data.append({
                "b_id": bay_id,
                "name": bay_name,
                "updated_at": datetime.now()
            })
        else:
            conn.execute(
                sa.update(table).where(
                    table.columns["id"] == sa.bindparam("b_id")
                ).values(
                    {
                        "name": sa.bindparam("name"),
                        "updated_at": sa.bindparam("updated_at")
                    }
                ),
                data
            )

    @classmethod
    def seed_components(cls):
        table = cls.__get_table('component')
        data = []
        conn = op.get_bind()
        equipment_table = cls.__get_table('equipment')
        equipment_type_table = cls.__get_table('equipment_type')

        equipments = conn.execute(
            sa.select(
                equipment_table.columns["id"],
                equipment_type_table.columns["name"]
            )
            .select_from(
                equipment_table.join(
                    equipment_type_table, equipment_table.columns["type_id"] == equipment_type_table.columns["id"]
                )
            )
        ).fetchall()

        sheet_data = cls.__get_anomalies_sheet()

        for equipment in equipments:
            data.extend([
                {
                    "name": component_name,
                    "equipment_id": equipment[0],
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                for component_name in sheet_data["equipments"][equipment[1]]["components"]
            ])
        op.bulk_insert(table, data)

    @classmethod
    def seed_component_possible_anomalies(cls):
        table = cls.__get_table('component_possible_anomalies')
        data = []
        conn = op.get_bind()
        component_table = cls.__get_table('component')
        equipment_table = cls.__get_table('equipment')
        anomaly_table = cls.__get_table('anomaly')
        equipment_type_table = cls.__get_table('equipment_type')

        components = conn.execute(
            sa.select(
                component_table.columns["id"],
                equipment_type_table.columns["name"]
            )
            .select_from(
                component_table
                .join(
                  equipment_table, component_table.columns["equipment_id"] == equipment_table.columns["id"]
                )
                .join(
                    equipment_type_table, equipment_table.columns["type_id"] == equipment_type_table.columns["id"]
                )
            )
        ).fetchall()

        anomalies = conn.execute(
            sa.select(
                anomaly_table.columns["id"],
                anomaly_table.columns["name"]
            )
        ).fetchall()

        sheet_data = cls.__get_anomalies_sheet()

        for component in components:
            anomaly_names = sheet_data["equipments"][component[1]]["anomalies"]
            possible_anomalies = [anomaly for anomaly in anomalies if anomaly[1] in anomaly_names]
            data.extend([
                {
                    "component_id": component[0],
                    "anomaly_id": anomaly[0],
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                for anomaly in possible_anomalies
            ])

        op.bulk_insert(table, data)
