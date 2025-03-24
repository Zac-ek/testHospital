const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
const mysql = require("mysql2/promise");
const app = express();
app.use(express.json());
app.use(cors()); // Activa CORS para todas las rutas

// Conexión a MongoDB
mongoose
  .connect(
    "mongodb+srv://raulreyesbatalla:Reyes53rrb53@raulrb.nay0eyj.mongodb.net/hospitalDB",
    {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    }
  )
  .then(() => console.log("Conectado a MongoDB"))
  .catch((err) => console.error("Error al conectar a MongoDB:", err));

// Definir el modelo para la colección "notas_medicas"
const notasMedicasSchema = new mongoose.Schema({}, { strict: false });
const notas_medicas = mongoose.model(
  "notas_medicas",
  notasMedicasSchema,
  "notas_medicas"
);

// Configuración de conexión para MySQL
const mysqlConfig = {
  host: "localhost",
  port: 3309,
  user: "root",
  password: "batman53",
  database: "hospital_general_8a_idgs_220217",
};

// Endpoint para obtener notas médicas desde MongoDB
// app.get("/api/mongo/notas", async (req, res) => {
//   try {
//     const notas = await notas_medicas.find();
//     res.json(notas);
//   } catch (err) {
//     res.status(500).json({ error: "Error al obtener datos de MongoDB" });
//   }
// });

// Endpoint para obtener usuarios desde MySQL
// app.get("/api/mysql/usuarios", async (req, res) => {
//   try {
//     const connection = await mysql.createConnection(mysqlConfig);
//     const [rows] = await connection.execute("SELECT * FROM tbb_usuarios");
//     await connection.end();
//     res.json(rows);
//   } catch (err) {
//     console.error(err);
//     res.status(500).json({ error: "Error al obtener datos de MySQL" });
//   }
// });

// Endpoint para obtener areas medicas desde MySQL
app.get("/api/mysql/estructura_hospital", async (req, res) => {
  try {
    const connection = await mysql.createConnection(mysqlConfig);

    // 1. Obtener las áreas (tbc_areas_medicas)
    const [areas] = await connection.execute(`
      SELECT ID, Nombre
      FROM tbc_areas_medicas
    `);

    // 2. Obtener todos los departamentos junto con el nombre completo del responsable
    const [depts] = await connection.execute(`
  SELECT 
     d.ID AS dept_id, 
     d.Nombre AS dept_nombre, 
     d.AreaMedica_ID, 
     d.departamento_superior_ID,
     CONCAT_WS(' ', p.Nombre, p.Primer_Apellido, p.Segundo_Apellido) AS responsable_nombre
  FROM tbc_departamentos d
  LEFT JOIN tbb_usuarios u ON d.Responsable_ID = u.ID
  LEFT JOIN tbb_personas p ON u.Persona_ID = p.ID
`);

    // 3. Obtener los médicos (doctores) de tbb_personal_medico
    // QUITA la primera consulta y renombra la segunda a doctores:
    const [doctores] = await connection.execute(`
  SELECT 
    pm.Persona_ID AS Personal_Medico_ID,
    pm.Departamento_ID,
    CONCAT_WS(' ', p.Nombre, p.Primer_Apellido, p.Segundo_Apellido) AS doctor_nombre
  FROM tbb_personal_medico pm
  LEFT JOIN tbb_personas p ON pm.Persona_ID = p.ID
  WHERE pm.Tipo = 'Médico'
`);

    // Ahora sí, "doctores" trae "Personal_Medico_ID"

    // 4. Obtener los enfermeros
    const [enfermeros] = await connection.execute(`
      SELECT 
        pm.Departamento_ID,
        CONCAT_WS(' ', p.Nombre, p.Primer_Apellido, p.Segundo_Apellido) AS enfermero_nombre
      FROM tbb_personal_medico pm
      LEFT JOIN tbb_personas p ON pm.Persona_ID = p.ID
      WHERE pm.Tipo = 'Enfermero'
    `);

    await connection.end();

    // Agrupar los doctores por Departamento_ID
    const doctorsByDept = {};
    doctores.forEach((doc) => {
      if (!doctorsByDept[doc.Departamento_ID]) {
        doctorsByDept[doc.Departamento_ID] = [];
      }
      doctorsByDept[doc.Departamento_ID].push({
        name: doc.doctor_nombre,
        value: 1,
        tipo: "doctor",
        personalId: doc.Personal_Medico_ID,
      });
    });

    // Agrupar los enfermeros por Departamento_ID
    const nursesByDept = {};
    enfermeros.forEach((enf) => {
      if (!nursesByDept[enf.Departamento_ID]) {
        nursesByDept[enf.Departamento_ID] = [];
      }
      nursesByDept[enf.Departamento_ID].push({
        name: enf.enfermero_nombre,
        value: 1,
        tipo: "enfermero",
        personalId: enf.Personal_Medico_ID,
      });
    });

    // Función que construye el árbol de departamentos (incluyendo subdepartamentos)
    function buildDeptTree(list) {
      const deptMap = {};
      // Crear nodo para cada departamento, guardando también el ID
      list.forEach((dept) => {
        deptMap[dept.dept_id] = {
          id: dept.dept_id,
          name: dept.dept_nombre,
          responsable: dept.responsable_nombre || "Sin responsable",
          children: [],
        };
      });
      const tree = [];
      list.forEach((dept) => {
        if (
          dept.departamento_superior_ID &&
          deptMap[dept.departamento_superior_ID]
        ) {
          deptMap[dept.departamento_superior_ID].children.push(
            deptMap[dept.dept_id]
          );
        } else {
          tree.push(deptMap[dept.dept_id]);
        }
      });
      return tree;
    }

    // Función recursiva para adjuntar nodos "Doctores" y "Enfermeros" a cada departamento
    function attachStaff(node) {
      // Adjuntar doctores si existen para este departamento
      if (doctorsByDept[node.id] && doctorsByDept[node.id].length > 0) {
        node.children.push({
          name: "Doctores",
          children: doctorsByDept[node.id],
          value: doctorsByDept[node.id].reduce(
            (acc, cur) => acc + cur.value,
            0
          ),
        });
      }
      // Adjuntar enfermeros si existen para este departamento
      if (nursesByDept[node.id] && nursesByDept[node.id].length > 0) {
        node.children.push({
          name: "Enfermeros",
          children: nursesByDept[node.id],
          value: nursesByDept[node.id].reduce((acc, cur) => acc + cur.value, 0),
        });
      }
      // Recursivamente aplicar a los hijos
      if (node.children && node.children.length > 0) {
        node.children.forEach((child) => attachStaff(child));
      }
    }

    // Construir la estructura final con "Hospital" como raíz
    const estructura = {
      name: "Hospital",
      responsable: "Director General", // Opcional, si lo deseas
      children: [],
    };

    // Filtrar las áreas que no se quieren mostrar (por ejemplo, Departamentos Administrativos y Servicios de Apoyo)
    const filteredAreas = areas.filter(
      (a) =>
        a.Nombre !== "Departamentos Administrativos" &&
        a.Nombre !== "Servicios de Apoyo"
    );

    // Para cada área filtrada, construir su árbol de departamentos y adjuntar el personal (doctores y enfermeros)
    filteredAreas.forEach((area) => {
      const areaDepts = depts.filter((d) => d.AreaMedica_ID === area.ID);
      const deptTree = buildDeptTree(areaDepts);
      deptTree.forEach((node) => attachStaff(node));
      estructura.children.push({
        name: area.Nombre,
        children: deptTree,
      });
    });

    res.json(estructura);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Error al obtener datos de MySQL" });
  }
});

// app.get("/api/mysql/usuarios_roles", async (req, res) => {
//   try {
//     const connection = await mysql.createConnection(mysqlConfig);
//     const [rows] = await connection.execute(`
//       SELECT ur.Usuario_ID, ur.Rol_ID, r.Nombre AS RoleName, ur.Estatus, ur.Fecha_Registro
//       FROM tbd_usuarios_roles ur
//       JOIN tbc_roles r ON ur.Rol_ID = r.ID
//     `);
//     await connection.end();
//     res.json(rows);
//   } catch (err) {
//     console.error(err);
//     res.status(500).json({ error: "Error al obtener datos de usuarios_roles" });
//   }
// });

// Configuración del puerto y arranque del servidor
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Servidor corriendo en el puerto ${port}`));